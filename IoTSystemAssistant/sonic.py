import RPi.GPIO as GPIO
import time

TRIG = 16
ECHO = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
time.sleep(0.5)


def measure_distance():
    # TRIG 핀에 10us 신호 보내기
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # ECHO가 HIGH가 될 때까지 대기
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # ECHO가 LOW가 될 때까지 대기
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # 시간 차이 계산
    pulse_duration = pulse_end - pulse_start

    # 거리 계산: 왕복 시간이므로 음속 / 2 적용
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


try:
    while True:
        dist = measure_distance()
        print("Distance:", dist, "cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping and cleaning up GPIO.")
    GPIO.cleanup()