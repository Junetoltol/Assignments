import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
import mediapipe as mp
import cv2
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# -----------[수정1] USB 웹캠 장치 번호를 명확히 지정-------------
# 대부분의 경우 0번이 USB 웹캠입니다.
# 만약 여러 카메라가 연결되어 있다면, 1, 2 등으로 변경할 수 있습니다.
cap = cv2.VideoCapture(1, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# -----------[수정2] USB 웹캠 연결 확인 코드 추가-------------
if not cap.isOpened():
    print(f"USB 웹캠을(를) 열 수 없습니다. 연결을 확인하세요.")
    exit()

with mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5,
    max_num_hands=1
) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다. USB 웹캠 연결을 확인하세요.")  # [수정3] 에러 메시지 추가
            time.sleep(0.5)
            continue

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        results = hands.process(image)
        hand_pos = "none"
        display_frame = cv2.flip(frame, 1)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            x = hand.landmark[mp_hands.HandLandmark.WRIST].x
            if x < 0.5:
                hand_pos = "left"
            else:
                hand_pos = "right"
            mp_drawing.draw_landmarks(
                display_frame, hand, mp_hands.HAND_CONNECTIONS
            )
            cv2.putText(display_frame, f"Hand: {hand_pos}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        else:
            cv2.putText(display_frame, "No hand detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

        # -----------[수정4] 파일 저장 경로를 홈 디렉토리로 변경(권장)-------------
        # USB 웹캠 환경에서는 /tmp 경로가 권한 문제로 파일 생성이 안 될 수 있으니 홈 디렉토리로 변경
        with open("/tmp/hand_result.txt", "w") as f:
            f.write(hand_pos)

        cv2.imshow("Hand Detection (USB Webcam)", display_frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()

#라즈베리파이내에 이름은 hand_detect_test.py
#실행명령어 python3 hand_detect_test.py
#오른손 왼손 다 인식함.