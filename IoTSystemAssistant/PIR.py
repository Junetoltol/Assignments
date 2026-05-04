import RPi.GPIO as GPIO
import time

PIR_input = 29

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_input, GPIO.IN)

motion_detected = False

try:
    while True:
        if GPIO.input(PIR_input):
            if not motion_detected:
                print("Motion detected!")
                motion_detected = True
        else:
            motion_detected = False

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()