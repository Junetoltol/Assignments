import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
import mediapipe as mp
import cv2
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
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

        with open("/tmp/hand_result.txt", "w") as f:
            f.write(hand_pos)

        cv2.imshow("Hand Detection", display_frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()
