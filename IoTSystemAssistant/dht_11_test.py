import time
import board
import adafruit_dht

# GPIO4 사용
dht = adafruit_dht.DHT11(board.D4)

while True:
    try:
        temperature = dht.temperature
        humidity = dht.humidity

        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")

    except RuntimeError as e:
        print("Read error:", e)

    time.sleep(2)