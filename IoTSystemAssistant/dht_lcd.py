import time
import board
import adafruit_dht
from RPLCD.i2c import CharLCD

# =========================
# Pin / Address Setting
# =========================

# DHT11 DATA pin is connected to GPIO4
dhtDevice = adafruit_dht.DHT11(board.D4)

# I2C LCD address
# If i2cdetect shows 27, use 0x27.
# If i2cdetect shows 3f, change this to 0x3f.
lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2,
    dotsize=8
)

# =========================
# LCD Initial Message
# =========================

lcd.clear()
lcd.write_string("DHT11 Sensor")
lcd.cursor_pos = (1, 0)
lcd.write_string("Starting...")
time.sleep(2)
lcd.clear()

try:
    while True:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity

            if temperature is not None and humidity is not None:
                lcd.clear()

                # First line: Temperature
                lcd.cursor_pos = (0, 0)
                lcd.write_string(f"Temp: {temperature:.1f}C")

                # Second line: Humidity
                lcd.cursor_pos = (1, 0)
                lcd.write_string(f"Humi: {humidity:.1f}%")

                print(f"Temp: {temperature:.1f} C, Humidity: {humidity:.1f}%")

            else:
                lcd.clear()
                lcd.write_string("Sensor Error")
                print("Sensor returned None")

        except RuntimeError as error:
            # DHT11 often gives temporary read errors
            print(f"Read error: {error}")

            lcd.clear()
            lcd.write_string("Read Error")
            lcd.cursor_pos = (1, 0)
            lcd.write_string("Retrying...")

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    lcd.clear()
    lcd.write_string("Stopped")
    dhtDevice.exit()
    time.sleep(1)
    lcd.clear()