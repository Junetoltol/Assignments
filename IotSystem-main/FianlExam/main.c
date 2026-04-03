#include "bt_master.h"
#include <unistd.h>
#include <wiringPi.h>
#include <stdio.h>
#include <wiringPi.h>
#include <string.h>      // strcmp(), strcpy() 사용을 위해
#include <math.h>        // pow() 함수
#include <wiringPiSPI.h> // SPI 함수

#define LED_PIN1 1
#define LED_PIN2 2
#define LED_PIN3 3
#define BUZZER_PIN 4
#define SPI_CH 0
#define ADC_CH 2
#define ADC_CS 29
#define SPI_SPEED 500000
#define Touch_Pin1 21
#define Touch_Pin2 22
#define Touch_Pin3 23

int Read_ADC(int adc_ch)
{
    unsigned char buf[3];
    int value;
    buf[0] = 0x06 | ((adc_ch & 0x04) >> 2);
    buf[1] = ((adc_ch & 0x03) << 6);
    buf[2] = 0x00;

    digitalWrite(ADC_CS, 0); // Start communication
    wiringPiSPIDataRW(SPI_CH, buf, 3);
    digitalWrite(ADC_CS, 1); // End communication

    buf[1] = 0x0F & buf[1];
    value = (buf[1] << 8) | buf[2];

    return value;
}

int delaytime(char *a)
{
    digitalWrite(LED_PIN1, LOW);
    digitalWrite(LED_PIN2, LOW);
    digitalWrite(LED_PIN3, LOW);
    int difficult;
    if (strcmp(a, "EASY") == 0)
    {
        difficult = 3000;
    }
    else if (strcmp(a, "NORMAL") == 0)
    {
        difficult = 2000;
    }
    else if (strcmp(a, "HARD") == 0)
    {
        difficult = 1000;
    }
    else
    {
        difficult = 5000;
    }

    printf("%d\n", difficult);
    delay(difficult);
    digitalWrite(LED_PIN1, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
    delay(difficult);
    digitalWrite(LED_PIN1, LOW);
    digitalWrite(LED_PIN2, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
    delay(difficult);
    digitalWrite(LED_PIN2, LOW);
    digitalWrite(LED_PIN3, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
    delay(difficult);
    digitalWrite(LED_PIN3, LOW);
    return difficult;
}

int random_LED()
{
    int randTemp = (rand() % 3) + 1;

    digitalWrite(LED_PIN1, LOW);
    digitalWrite(LED_PIN2, LOW);
    digitalWrite(LED_PIN3, LOW);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
    switch (randTemp)
    {
    case 1:
        digitalWrite(LED_PIN1, HIGH);
        break;
    case 2:
        digitalWrite(LED_PIN2, HIGH);
        break;
    case 3:
        digitalWrite(LED_PIN3, HIGH);
        break;
    }
    printf("radomTemp = %d\n", randTemp);
    return randTemp;
}

int problem(int di, int N, int Bu)
{
    delay(di);
    if (N == Bu)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}
/*
int read_hand_position() {
    FILE *fp = fopen("/tmp/hand_result.txt", "r");
    if (!fp) return 0; // 파일 없음
    char buf[16] = {0};
    fgets(buf, sizeof(buf), fp);
    fclose(fp);
    if (strncmp(buf, "left", 4) == 0) return 1;
    if (strncmp(buf, "right", 5) == 0) return 2;
    return 0; // none
}
    //손 인식 코드. 
*/
int main()
{
    int client = init_server();
    int d, LED_N, answer, check_button;
    int check_Number;
    char *recv_message;
    char difficulty[16];
    char *send_message[100];

    if (wiringPiSetup() == -1)
    {
        return 1;
    }
    // 기존: wiringPiSPISetup() → 인자 누락
    if (wiringPiSPISetup(SPI_CH, SPI_SPEED) == -1)
        return -1;

    pinMode(ADC_CS, OUTPUT);
    pinMode(LED_PIN1, OUTPUT);
    pinMode(LED_PIN2, OUTPUT);
    pinMode(LED_PIN3, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(Touch_Pin3, INPUT);
    pullUpDnControl(Touch_Pin3, PUD_DOWN);

    while (1)
    {
        recv_message = read_server(client);

        strcpy(difficulty, recv_message);

        if (strcmp(difficulty, "EASY") == 0 ||
            strcmp(difficulty, "NORMAL") == 0 ||
            strcmp(difficulty, "HARD") == 0)
        {
            strcpy(recv_message, "시작!\n");
            d = delaytime(difficulty);
            LED_N = random_LED();
            // Wait for one of the buttons to be pressed
            while (1)
            {
                if (digitalRead(Touch_Pin1) == HIGH)
                {
                    check_button = 1;
                    break;
                }
                else if (digitalRead(Touch_Pin2) == HIGH)
                {
                    check_button = 2;
                    break;
                }
                else if (digitalRead(Touch_Pin3) == HIGH)
                {
                    check_button = 3;
                    break;
                }
            }
            /*
            //버튼대신 손 드는것
            printf("손을 들어 올려주세요! (왼손: 1, 오른손: 2)\n");
            while (1)
            {
                check_button = read_hand_position(); // 손 인식 결과 읽기
                if (check_button == 1 || check_button == 2)
                {
                    break;
                }
                delay(100); // 0.1초 대기
            }
            */
            delay(100); // Debounce
            printf("Button pressed: %d\n", check_button);

            strcpy(recv_message, "종료!\n");
            printf("종료!\n");
        }
        else
        {
            printf("client disconnected\n");
            break;
        }
        write_server(client, recv_message);
    }
}

/*
python3 hand_detect.py
sudo ./fm

read_hand_position 함수

/tmp/hand_result.txt 파일을 읽어서 손의 위치를 판별.

left → 1, right → 2, none → 0

*/