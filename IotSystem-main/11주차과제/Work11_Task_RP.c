#include "bt_master.h"
#include <unistd.h>
#include <wiringPi.h>
#include <unistd.h>
#include <stdio.h>
#include <wiringPi.h>

#define LED_PIN 1
#define PIR_PIN 2
#define SPI_CH 0
#define ADC_CH 2       // Changed to ADC Channel 1
#define ADC_CS 29
#define SPI_SPEED  500000
#define DC_PIN 5 //DC모터
#define Gas_sensor 0
#define Dust_sensor 1

int Read_ADC(int adc_ch){
    unsigned char buf[3];
    int value;
     buf[0] = 0x06|((adc_ch&0x04)>>2);
     buf[1] = ((adc_ch&0x03)<<6);
     buf[2] = 0x00;

    digitalWrite(ADC_CS, 0);                         // Start communication
    wiringPiSPIDataRW(SPI_CH, buf, 3);
    digitalWrite(ADC_CS, 1);                         // End communication

    buf[1] = 0x0F & buf[1];
    value = (buf[1] << 8) | buf[2];

    return value;
}

int main()
{
    int client = init_server();
    int pir,value=0;
    char *recv_message;
    char *send_message[100];

    if (wiringPiSetup() == -1)
    {
        return 1;
     }
    if(wiringPiSPISetup()==-1)return -1;

    pinMode(PIR_PIN,INPUT);
    pinMode(Gas_sensor,INPUT);
    pinMode(Dust_sensor,INPUT);
    pinMode(ADC_CS,OUTPUT);
    pinMode(LED_PIN, OUTPUT);
    pinMode(DC_PIN,OUTPUT);

    while (1)
    {
        recv_message = read_server(client);
        if (recv_message == NULL)
        {
            printf("client disconnected\n");
            break;
        }
        if (strcmp(recv_message, "PIR") == 0)
        {
            pir = digitalRead(PIR_PIN);
            if(pir == HIGH)
            {
                strcpy(recv_message, "PIR - Detected!!\n");
            }
            else if(pir == LOW)
            {
                strcpy(recv_message, "PIR - UnDetected!!\n");
            }
        }
        if (strcmp(recv_message, "LEDON") == 0)
        {
                digitalWrite(LED_PIN, HIGH);
                strcpy(recv_message, "LED ON!\n");
        }
        else if (strcmp(recv_message, "LEDOFF") == 0)
        {
            digitalWrite(LED_PIN, LOW);
            strcpy(recv_message, "LED OFF!\n");
        }
        if (strcmp(recv_message, "DCON") == 0)
        {
            digitalWrite(DC_PIN,HIGH);
            strcpy(recv_message, "DC ON!\n");
        }
        else if (strcmp(recv_message, "DCOFF") == 0)
  {
            digitalWrite(DC_PIN,LOW);
            strcpy(recv_message, "DC OFF!\n");
        }
        if (strcmp(recv_message, "GASON") == 0)
        {
            value = Read_ADC(Gas_sensor);
            printf("%d\n",value);
            sprintf(recv_message, "%d\n", value);
        }
        if (strcmp(recv_message, "DUSTON") == 0)
        {
            delay(280);
            value = Read_ADC(Dust_sensor);
            sprintf(recv_message, "%d\n", value);
        }
       write_server(client, recv_message);
    }
}
