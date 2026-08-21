import argparse
import subprocess
import time
from pathlib import Path

import cv2
import numpy as np
from gpiozero import Buzzer
from RPLCD.i2c import CharLCD


# =========================
# 기본 설정
# =========================

BUZZER_PIN = 17          # 버저 GPIO 핀: BCM 17
LCD_I2C_ADDRESS = 0x27   # LCD 주소. 안 되면 0x3f로 변경
LCD_COLS = 16
LCD_ROWS = 2


COLOR_NAMES_KR = {
    "red": "RED",
    "orange": "ORANGE",
    "yellow": "YELLOW",
    "green": "GREEN",
    "cyan": "CYAN",
    "blue": "BLUE",
    "purple": "PURPLE",
    "pink": "PINK",
    "brown": "BROWN",
    "black": "BLACK",
    "white": "WHITE",
    "gray": "GRAY",
    "unknown": "UNKNOWN",
}


def capture_image(output_path="capture.jpg"):
    """
    Raspberry Pi 카메라로 사진 촬영.
    SSH 환경에서도 동작하도록 -n 옵션으로 preview를 끈다.
    """
    cmd = [
        "rpicam-still",
        "-n",
        "-t", "1000",
        "-o", output_path,
    ]

    print("[INFO] Capturing image...")

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print("[ERROR] Camera capture failed.")
        print(result.stderr)
        raise RuntimeError("rpicam-still failed")

    print(f"[INFO] Image saved: {output_path}")
    return output_path


def get_center_roi(image, roi_ratio=0.6):
    """
    배경 영향을 줄이기 위해 이미지 중앙 영역만 분석한다.
    """
    h, w = image.shape[:2]

    roi_w = int(w * roi_ratio)
    roi_h = int(h * roi_ratio)

    x1 = (w - roi_w) // 2
    y1 = (h - roi_h) // 2
    x2 = x1 + roi_w
    y2 = y1 + roi_h

    return image[y1:y2, x1:x2]


def classify_dominant_color(image_bgr):
    """
    BGR 이미지를 HSV 색공간으로 변환한 뒤 대표 색상 하나를 판단한다.
    """
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    masks = {}

    # 무채색 계열
    masks["black"] = v < 45
    masks["white"] = (s < 35) & (v > 200)
    masks["gray"] = (s < 45) & (v >= 45) & (v <= 200)

    # 유채색 후보
    valid = (s >= 45) & (v >= 45)

    # 갈색: 어두운 주황/노랑 계열
    masks["brown"] = valid & (h >= 5) & (h <= 28) & (v < 165) & (s >= 50)

    # 일반 색상
    masks["red"] = valid & ((h <= 10) | (h >= 170))
    masks["orange"] = valid & (h >= 11) & (h <= 22)
    masks["yellow"] = valid & (h >= 23) & (h <= 34)
    masks["green"] = valid & (h >= 35) & (h <= 85)
    masks["cyan"] = valid & (h >= 86) & (h <= 99)
    masks["blue"] = valid & (h >= 100) & (h <= 125)
    masks["purple"] = valid & (h >= 126) & (h <= 145)
    masks["pink"] = valid & (h >= 146) & (h <= 169)

    color_counts = {}

    for color_name, mask in masks.items():
        color_counts[color_name] = int(np.count_nonzero(mask))

    dominant_color = max(color_counts, key=color_counts.get)

    total_pixels = image_bgr.shape[0] * image_bgr.shape[1]
    dominant_ratio = color_counts[dominant_color] / total_pixels

    # 너무 애매하면 unknown 처리
    if dominant_ratio < 0.05:
        dominant_color = "unknown"

    return dominant_color, dominant_ratio


def init_lcd(i2c_address):
    """
    I2C LCD 초기화.
    일반적인 PCF8574 I2C LCD 기준.
    """
    lcd = CharLCD(
        i2c_expander="PCF8574",
        address=i2c_address,
        port=1,
        cols=LCD_COLS,
        rows=LCD_ROWS,
        charmap="A00",
        auto_linebreaks=True
    )

    lcd.clear()
    return lcd


def display_lcd(lcd, color, ratio, alarm_color):
    """
    LCD에 대표 색상과 버저 상태 출력.
    """
    lcd.clear()

    color_text = COLOR_NAMES_KR.get(color, "UNKNOWN")
    ratio_percent = ratio * 100

    line1 = f"Color:{color_text}"
    line2 = f"Rate:{ratio_percent:5.1f}%"

    if color == alarm_color:
        line2 = "BUZZER: ON"

    lcd.write_string(line1[:16])
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2[:16])


def buzz_alert(buzzer, duration=1.0):
    """
    능동 부저 기준.
    GPIO HIGH가 되면 소리가 나는 부저에 적합하다.
    """
    buzzer.on()
    time.sleep(duration)
    buzzer.off()


def main():
    parser = argparse.ArgumentParser(
        description="Color detection with LCD and buzzer"
    )

    parser.add_argument(
        "--image",
        type=str,
        default="",
        help="이미 촬영된 이미지 파일을 분석. 비워두면 새로 촬영함."
    )

    parser.add_argument(
        "--alarm",
        type=str,
        default="red",
        choices=[
            "red", "orange", "yellow", "green", "cyan", "blue",
            "purple", "pink", "brown", "black", "white", "gray"
        ],
        help="버저가 울릴 색상. 기본값: red"
    )

    parser.add_argument(
        "--lcd",
        type=str,
        default="0x27",
        help="LCD I2C 주소. 기본값: 0x27. 예: 0x3f"
    )

    parser.add_argument(
        "--roi",
        type=float,
        default=0.6,
        help="중앙 분석 영역 비율. 기본값: 0.6"
    )

    args = parser.parse_args()

    lcd_address = int(args.lcd, 16)

    # LCD / Buzzer 초기화
    lcd = init_lcd(lcd_address)
    buzzer = Buzzer(BUZZER_PIN)

    try:
        lcd.write_string("Color Detector")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Starting...")
        time.sleep(1)

        # 1. 이미지 준비
        if args.image:
            image_path = args.image
            print(f"[INFO] Using existing image: {image_path}")
        else:
            image_path = capture_image("capture.jpg")

        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        # 2. 이미지 읽기
        image = cv2.imread(image_path)

        if image is None:
            raise RuntimeError(f"Failed to read image: {image_path}")

        # 3. 중앙 영역 분석
        roi = get_center_roi(image, args.roi)

        # 4. 대표 색상 판단
        dominant_color, dominant_ratio = classify_dominant_color(roi)

        print("================================")
        print(f"Dominant Color: {dominant_color}")
        print(f"Ratio: {dominant_ratio * 100:.2f}%")
        print(f"Alarm Color: {args.alarm}")
        print("================================")

        # 5. LCD 출력
        display_lcd(lcd, dominant_color, dominant_ratio, args.alarm)

        # 6. 특정 색상일 때 버저 울림
        if dominant_color == args.alarm:
            print("[RESULT] Alarm color detected. Buzzer ON.")
            buzz_alert(buzzer, duration=1.0)
        else:
            print("[RESULT] Normal color detected. Buzzer OFF.")
            buzzer.off()

        time.sleep(2)

    finally:
        buzzer.off()
        # LCD 화면은 결과를 남겨두고 싶으면 clear하지 않는다.
        # 종료할 때 지우고 싶으면 아래 주석을 해제한다.
        # lcd.clear()


if __name__ == "__main__":
    main()