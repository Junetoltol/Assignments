#include "bt_master.h"
#include <unistd.h>
#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>
#include <wiringPi.h>

#define PIN 2
#define SPI_CH     0
#define ADC_CH     2       // Changed to ADC Channel 1
#define ADC_CS     29
#define SPI_SPEED  500000

int main()
{
    int client = init_server();
    int pir,value;
    int adcValue = 0;
    char *recv_message;
    char *send_message[100];
    unsigned char buf[3];

    if (wiringPiSetup() == -1)
    {
        return 1;
    }
    if(wiringPiSPISetup()==-1)return -1;
    pinMode(PIN, INPUT);
    pinMode(ADC_CS,OUTPUT);
    while (1)
    {

        recv_message = read_server(client);
        if (recv_message == NULL)
        {
            printf("client disconnected\n");
            break;
        }
        if (strcmp(recv_message, "PIN") == 0)
        {
            pir = digitalRead(PIN);
            if(pir == HIGH)
            {
                strcpy(recv_message, "PIR - Detected!!\n");
            }
            else if(pir == LOW)
            {
                strcpy(recv_message, "PIR - UnDetected!!\n");
            }
        }
        if (strcmp(recv_message, "SOUND") == 0)
        {
        buf[0] = 0x06|((ADC_CH&0x04)>>2);
        buf[1] = ((ADC_CH&0x03)<<6);
        buf[2] = 0x00;
        digitalWrite(ADC_CS,0);
        wiringPiSPIDataRW(SPI_CH,buf,3);
        buf[1] = 0x0F & buf[1];
        value = (buf[1]<<8) | buf[2];
        digitalWrite(ADC_CS,1);
        sprintf(recv_message,"%d\n",adcValue);
        }
        write_server(client, recv_message);
    }
}