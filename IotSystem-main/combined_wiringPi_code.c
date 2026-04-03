
#include <wiringPi.h>
#include <stdio.h>
#include <wiringPiSPI.h>  // SPI 함수 (wiringPiSPISetup, wiringPiSPIDataRW)
#include <unistd.h>       // usleep 함수
#include <math.h>         // pow 함수
#include <crypt.h>        // crypt 함수 (필요시)

// 일반 입출력 설정용
#define PIN_INPUT 2
#define PIN_OUT1 7
#define PIN_OUT2 26

// SPI ADC 설정
#define SPI_CH 0
#define ADC_CH 2
#define ADC_CS 29
#define SPI_SPEED 500000

// 모터 제어용 핀
#define PIN_1A 27
#define PIN_1B 0
#define PIN_2A 1
#define PIN_2B 24

int main(void) {
    // 1. 기본 GPIO 설정
    if (wiringPiSetup() == -1) return 1;

    // 2. 일반 입출력 핀 설정
    pinMode(PIN_OUT1, OUTPUT);
    digitalWrite(PIN_OUT1, LOW);
    printf("PIN_OUT1: 0\n");

    pinMode(PIN_OUT2, OUTPUT);
    digitalWrite(PIN_OUT2, HIGH);
    printf("PIN_OUT2: 1\n");

    pinMode(PIN_INPUT, INPUT);
    printf("PIN_INPUT: %d\n", digitalRead(PIN_INPUT));

    // 3. SPI ADC 데이터 읽기
    int value = 0;
    unsigned char buf[3];

    if (wiringPiSPISetup(SPI_CH, SPI_SPEED) == -1) return -1;

    pinMode(ADC_CS, OUTPUT);
    buf[0] = 0x06 | ((ADC_CH & 0x04) >> 2);
    buf[1] = ((ADC_CH & 0x03) << 6);
    buf[2] = 0x00;

    digitalWrite(ADC_CS, 0);
    wiringPiSPIDataRW(SPI_CH, buf, 3);
    buf[1] = 0x0F & buf[1];
    value = (buf[1] << 8) | buf[2];
    digitalWrite(ADC_CS, 1);
    printf("ADC Value: %d\n", value);

    // 4. 모터 핀 설정 및 제어 루프
    pinMode(PIN_1A, OUTPUT);
    pinMode(PIN_1B, OUTPUT);
    pinMode(PIN_2A, OUTPUT);
    pinMode(PIN_2B, OUTPUT);

    int i;
    for (i = 0; i < 500; i++) {
        digitalWrite(PIN_1A, HIGH);
        digitalWrite(PIN_1B, LOW);
        digitalWrite(PIN_2A, LOW);
        digitalWrite(PIN_2B, LOW);
        usleep(8000);

        digitalWrite(PIN_1A, LOW);
        digitalWrite(PIN_1B, HIGH);
        digitalWrite(PIN_2A, LOW);
        digitalWrite(PIN_2B, LOW);
        usleep(8000);

        digitalWrite(PIN_1A, LOW);
        digitalWrite(PIN_1B, LOW);
        digitalWrite(PIN_2A, HIGH);
        digitalWrite(PIN_2B, LOW);
        usleep(8000);

        digitalWrite(PIN_1A, LOW);
        digitalWrite(PIN_1B, LOW);
        digitalWrite(PIN_2A, LOW);
        digitalWrite(PIN_2B, HIGH);
        usleep(8000);
    }

    printf("모든 동작 완료\n");
    return 0;
}
//gcc -o combined_wiringPi combined_wiringPi_code.c -lwiringPi -lm -lcrypt -lpthread
