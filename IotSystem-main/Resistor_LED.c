#include <stdio.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>

#define SPI_CH     0
#define ADC_CH     1       // Changed to ADC Channel 1
#define ADC_CS     29
#define SPI_SPEED  500000
#define PIN 7

int readADC(int adcChannel) {
    unsigned char buf[3];
    int value;

    buf[0] = 0x06 | ((adcChannel & 0x04) >> 2);
    buf[1] = ((adcChannel & 0x03) << 6);
    buf[2] = 0x00;

    digitalWrite(ADC_CS, 0);                         // Start communication
    wiringPiSPIDataRW(SPI_CH, buf, 3);
    digitalWrite(ADC_CS, 1);                         // End communication

    buf[1] = 0x0F & buf[1];
    value = (buf[1] << 8) | buf[2];

    return value;
}

int main(void) {
    int i, value;

    if (wiringPiSetup() == -1)
        return 1;
    if (wiringPiSPISetup(SPI_CH, SPI_SPEED) == -1)
        return -1;
    wiringPiSPIDataRW(SPI_CH, buf, 3);
    digitalWrite(ADC_CS, 1);                         // End communication

    buf[1] = 0x0F & buf[1];
    value = (buf[1] << 8) | buf[2];

    return value;
}

int main(void) {
    int i, value;

    if (wiringPiSetup() == -1)
        return 1;
    if (wiringPiSPISetup(SPI_CH, SPI_SPEED) == -1)
        return -1;

    pinMode(ADC_CS, OUTPUT);
    pinMode(PIN,OUTPUT);

    for (i = 0; i < 100; i++) {
        value = readADC(ADC_CH);     // Use the function with ADC channel 1
        printf("%d\n", value);
        if (value >30){
        digitalWrite(PIN,HIGH);
        }
        else{
        digitalWrite(PIN,LOW);
        }
        delay(100);
    }

    return 0;
}

