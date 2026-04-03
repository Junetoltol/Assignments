# color_detect.py
import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 빨강 영역 (HSV)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # 초록 영역 (HSV)
    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # 파랑 영역 (HSV)
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # 각 색의 픽셀 수 계산
    red_count = cv2.countNonZero(mask_red)
    green_count = cv2.countNonZero(mask_green)
    blue_count = cv2.countNonZero(mask_blue)

    color = "none"
    if max(red_count, green_count, blue_count) > 1000:  # 임계값 조정 가능
        if red_count == max(red_count, green_count, blue_count):
            color = "red"
        elif green_count == max(red_count, green_count, blue_count):
            color = "green"
        else:
            color = "blue"

    # 결과 파일에 기록
    with open("/tmp/color_result.txt", "w") as f:
        f.write(color)

    # (옵션) 화면 표시 부분 제거됨

    time.sleep(0.1)

cap.release()

"""
처음 설치해야할 것들.

sudo apt-get update
sudo apt-get upgrade
sudo reboot

sudo apt-get install ffmpeg python3-opencv
sudo apt-get install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1 libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b
sudo apt-get install libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23

파이썬으로 색깔을 인식해서 /tmp/color_result.txt 에 저장하는 것임.
"""