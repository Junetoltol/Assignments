import json
import os
import time

import RPi.GPIO as GPIO
from azure.iot.device import IoTHubDeviceClient, Message

# ==========================================
# Azure IoT Hub Connection String
# ==========================================
CONNECTION_STRING = os.environ.get("AZURE_IOT_DEVICE_CONNECTION_STRING")

if not CONNECTION_STRING:
    raise RuntimeError(
        "AZURE_IOT_DEVICE_CONNECTION_STRING environment variable is required."
    )
# ==========================================
# GPIO Setup
# ==========================================
VIBRATION_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(VIBRATION_PIN, GPIO.IN)

# ==========================================
# Azure Client
# ==========================================
client = None
vibration_count = 0

try:
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    client.connect()

    print("Azure IoT Hub Connected")
    print("Monitoring vibration sensor...")

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
    if client is not None:
        client.disconnect()
    GPIO.cleanup()
