# hand_detect.py
import mediapipe as mp
import cv2
import time

mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5,
    max_num_hands=1
) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        results = hands.process(image)
        hand_pos = "none"

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            x = hand.landmark[mp_hands.HandLandmark.WRIST].x
            if x < 0.5:
                hand_pos = "left"
            else:
                hand_pos = "right"
        with open("/tmp/hand_result.txt", "w") as f:
            f.write(hand_pos)
        time.sleep(0.1)

#https://github.com/Physicslibrary/Raspberry-Pi-MediaPipe-Experiment/blob/b69cf710ed5e5443dfa201024ce2329853dfcf1d/README.md
"""
처음 설치해야할 것들.

sudo apt-get update
sudo apt-get upgrade
sudo reboot

sudo apt-get install ffmpeg python3-opencv
sudo apt-get install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1 libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b
sudo apt-get install libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23

파이썬으로 양손을 인식해서 /tmp/hand_result.txt 에 저장하는 것임.
"""