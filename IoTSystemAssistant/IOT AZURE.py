import RPi.GPIO as GPIO
import time
import json
from azure.iot.device import IoTHubDeviceClient, Message

# ==========================================
# Azure IoT Hub Connection String
# ==========================================
CONNECTION_STRING = ""
# ==========================================
# GPIO Setup
# ==========================================
VIBRATION_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(VIBRATION_PIN, GPIO.IN)

# ==========================================
# Azure Client
# ==========================================
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
client.connect()

print("Azure IoT Hub Connected")
print("Monitoring vibration sensor...")

vibration_count = 0

try:
    while True:
        vibration = GPIO.input(VIBRATION_PIN)

        if vibration == 1:
            vibration_count += 1

            data = {
                "sensor": "vibration",
                "status": "DETECTED",
                "count": vibration_count,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

            message = Message(json.dumps(data))
            client.send_message(message)

            print("Vibration Detected!")
            print(f"Count: {vibration_count}")
            print("Message successfully sent")
            print(data)

            time.sleep(0.5)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    client.disconnect()
    GPIO.cleanup()