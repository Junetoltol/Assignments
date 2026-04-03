#include "bt_master.h"
#include <unistd.h>
#include <wiringPi.h>
#define PIN 2
int main()
{
    int client = init_server();
    int pir;
    char *recv_message;
    char *send_message;

    if (wiringPiSetup() == -1)
    {
        return 1;
    }
    pinMode(PIN, INPUT);
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
            pir = digitalRead(PIN);
        }
        if(pir == HIGH){
            strcpy(recv_message,"PIR - Detected!\n");
        }
        else if(pir == LOW){
            strcpy(recv_message,"PIR - Undetected..\n");
        }
        write_server(client, recv_message);
    }
}