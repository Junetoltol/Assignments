import argparse
import subprocess
from pathlib import Path

import cv2
import numpy as np


COLOR_NAMES_KR = {
    "red": "빨강",
    "orange": "주황",
    "yellow": "노랑",
    "green": "초록",
    "cyan": "하늘색",
    "blue": "파랑",
    "purple": "보라",
    "pink": "분홍",
    "brown": "갈색",
    "black": "검정",
    "white": "흰색",
    "gray": "회색",
    "unknown": "기타",
}


DRAW_COLORS_BGR = {
    "red": (0, 0, 255),
    "orange": (0, 140, 255),
    "yellow": (0, 255, 255),
    "green": (0, 255, 0),
    "cyan": (255, 255, 0),
    "blue": (255, 0, 0),
    "purple": (255, 0, 150),
    "pink": (180, 0, 255),
    "brown": (30, 90, 150),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "gray": (130, 130, 130),
    "unknown": (80, 80, 80),
}


def capture_image(output_path: str, width: int = 1280, height: int = 720, delay_ms: int = 1000):
    """
    rpicam-still을 이용해서 사진을 촬영한다.
    SSH 환경이므로 -n 옵션으로 preview를 끈다.
    """
    cmd = [
        "rpicam-still",
        "-n",
        "-t", str(delay_ms),
        "--width", str(width),
        "--height", str(height),
        "-o", output_path,
    ]

    print("[INFO] Capturing image...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("[ERROR] Camera capture failed.")
        print(result.stderr)
        raise RuntimeError("rpicam-still failed")

    print(f"[INFO] Image saved: {output_path}")


def get_center_roi(image: np.ndarray, roi_ratio: float):
    """
    이미지 중앙 영역만 잘라낸다.
    배경 영향을 줄이기 위해 기본값은 중앙 60% 영역이다.
    """
    h, w = image.shape[:2]

    roi_w = int(w * roi_ratio)
    roi_h = int(h * roi_ratio)

    x1 = (w - roi_w) // 2
    y1 = (h - roi_h) // 2
    x2 = x1 + roi_w
    y2 = y1 + roi_h

    roi = image[y1:y2, x1:x2]

    return roi, (x1, y1, x2, y2)


def classify_colors_bgr(image_bgr: np.ndarray):
    """
    BGR 이미지를 HSV로 변환한 뒤 색상별 마스크를 만든다.
    OpenCV HSV 범위:
    H: 0~179
    S: 0~255
    V: 0~255
    """
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    total_pixels = h.size
    assigned = np.zeros(h.shape, dtype=bool)

    masks = {}

    # 1. 밝기/채도 기반 무채색 먼저 분류
    masks["black"] = v < 45
    assigned |= masks["black"]

    masks["white"] = (s < 35) & (v > 200) & (~assigned)
    assigned |= masks["white"]

    masks["gray"] = (s < 45) & (v >= 45) & (v <= 200) & (~assigned)
    assigned |= masks["gray"]

    # 2. 유채색 후보
    valid = (s >= 45) & (v >= 45) & (~assigned)

    # 갈색은 주황/노랑 계열이면서 어두운 색이므로 먼저 분류
    masks["brown"] = valid & (h >= 5) & (h <= 28) & (v < 165) & (s >= 50)
    assigned |= masks["brown"]

    # 빨강은 HSV에서 0 근처와 179 근처가 나뉜다.
    masks["red"] = valid & (~assigned) & ((h <= 10) | (h >= 170))
    assigned |= masks["red"]

    masks["orange"] = valid & (~assigned) & (h >= 11) & (h <= 22)
    assigned |= masks["orange"]

    masks["yellow"] = valid & (~assigned) & (h >= 23) & (h <= 34)
    assigned |= masks["yellow"]

    masks["green"] = valid & (~assigned) & (h >= 35) & (h <= 85)
    assigned |= masks["green"]

    masks["cyan"] = valid & (~assigned) & (h >= 86) & (h <= 99)
    assigned |= masks["cyan"]

    masks["blue"] = valid & (~assigned) & (h >= 100) & (h <= 125)
    assigned |= masks["blue"]

    masks["purple"] = valid & (~assigned) & (h >= 126) & (h <= 145)
    assigned |= masks["purple"]

    masks["pink"] = valid & (~assigned) & (h >= 146) & (h <= 169)
    assigned |= masks["pink"]

    masks["unknown"] = ~assigned

    percentages = {}
    counts = {}

    for color_name, mask in masks.items():
        count = int(np.count_nonzero(mask))
        percent = count / total_pixels * 100
        counts[color_name] = count
        percentages[color_name] = percent

    return percentages, counts, masks


def get_dominant_color(percentages: dict):
    """
    기타 unknown을 제외하고 가장 비율이 높은 색을 대표 색상으로 정한다.
    """
    filtered = {
        color: percent
        for color, percent in percentages.items()
        if color != "unknown"
    }

    dominant = max(filtered, key=filtered.get)
    return dominant, filtered[dominant]


def draw_result(image_bgr: np.ndarray, roi_box, dominant_color: str, dominant_percent: float, output_path: str):
    """
    원본 이미지에 ROI 박스와 대표 색상 결과를 표시해서 저장한다.
    """
    result = image_bgr.copy()
    x1, y1, x2, y2 = roi_box

    cv2.rectangle(result, (x1, y1), (x2, y2), (0, 255, 255), 3)

    text = f"Dominant: {COLOR_NAMES_KR[dominant_color]} ({dominant_percent:.1f}%)"
    cv2.putText(
        result,
        text,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        DRAW_COLORS_BGR.get(dominant_color, (255, 255, 255)),
        3,
        cv2.LINE_AA,
    )

    cv2.imwrite(output_path, result)
    print(f"[INFO] Result image saved: {output_path}")


def print_percentages(percentages: dict):
    """
    색상 비율을 보기 좋게 출력한다.
    """
    print("\n========== Color Percentage Result ==========")

    sorted_items = sorted(
        percentages.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for color_name, percent in sorted_items:
        kr_name = COLOR_NAMES_KR[color_name]
        print(f"{kr_name:>4s} / {color_name:<8s}: {percent:6.2f}%")

    print("============================================\n")


def save_report(percentages: dict, dominant_color: str, dominant_percent: float, report_path: str):
    """
    분석 결과를 txt 파일로 저장한다.
    """
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("Color Detection Report\n")
        f.write("======================\n\n")
        f.write(f"Dominant color: {COLOR_NAMES_KR[dominant_color]} / {dominant_color}\n")
        f.write(f"Dominant percent: {dominant_percent:.2f}%\n\n")
        f.write("Color percentages:\n")

        sorted_items = sorted(
            percentages.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for color_name, percent in sorted_items:
            f.write(f"{COLOR_NAMES_KR[color_name]} / {color_name}: {percent:.2f}%\n")

    print(f"[INFO] Report saved: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Raspberry Pi camera color detector")

    parser.add_argument(
        "--image",
        type=str,
        default="",
        help="이미 촬영된 이미지 파일을 분석할 때 사용. 비워두면 새로 촬영함."
    )

    parser.add_argument(
        "--capture",
        type=str,
        default="capture.jpg",
        help="촬영 이미지 저장 파일명"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="color_result.jpg",
        help="분석 결과 이미지 저장 파일명"
    )

    parser.add_argument(
        "--report",
        type=str,
        default="color_report.txt",
        help="분석 결과 txt 저장 파일명"
    )

    parser.add_argument(
        "--roi",
        type=float,
        default=0.6,
        help="중앙 분석 영역 비율. 기본값 0.6"
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="중앙 영역이 아니라 전체 이미지를 분석"
    )

    args = parser.parse_args()

    # 1. 이미지 준비
    if args.image:
        image_path = args.image
        print(f"[INFO] Using existing image: {image_path}")
    else:
        image_path = args.capture
        capture_image(image_path)

    if not Path(image_path).exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # 2. 이미지 읽기
    image_bgr = cv2.imread(image_path)

    if image_bgr is None:
        raise RuntimeError(f"Failed to read image: {image_path}")

    # 3. ROI 선택
    if args.full:
        roi = image_bgr
        h, w = image_bgr.shape[:2]
        roi_box = (0, 0, w, h)
        print("[INFO] Analyzing full image.")
    else:
        roi, roi_box = get_center_roi(image_bgr, args.roi)
        print(f"[INFO] Analyzing center ROI: {args.roi * 100:.0f}%")

    # 4. 색상 분석
    percentages, counts, masks = classify_colors_bgr(roi)

    # 5. 대표 색상 계산
    dominant_color, dominant_percent = get_dominant_color(percentages)

    # 6. 결과 출력
    print_percentages(percentages)

    print(f"[RESULT] Dominant color: {COLOR_NAMES_KR[dominant_color]} / {dominant_color}")
    print(f"[RESULT] Dominant percent: {dominant_percent:.2f}%")

    # 7. 결과 저장
    draw_result(image_bgr, roi_box, dominant_color, dominant_percent, args.output)
    save_report(percentages, dominant_color, dominant_percent, args.report)


if __name__ == "__main__":
    main()