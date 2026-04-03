#include<stdio.h>
#include<wiringPi.h>
#define TRIG 28
#define OUT 29

int main(void){
        int dis =0, i;
        long start,travel;
        if(wiringPiSetup() == -1) return 1;
        pinMode(TRIG,OUTPUT);
        pinMode(OUT,INPUT);

        for(i=0;i<20;i++){
        //TRIG pin must LOW
        digitalWrite(TRIG,0);
        //WAIT for Sensor to settle
        usleep(2);

        //send trig pluse
        digitalWrite(TRIG,1);
        usleep(20);
        digitalWrite(TRIG,0);

        //wait for echo start
        while(digitalRead(OUT)==0);

        start = micros();
        //wait for echo end
        while(digitalRead(OUT) == 1);

        travel = micros() - start;

        ///spend of sound 340 m/s = 29 microsecond/cm
        //Sound wavge reflect frome the obstacle, so to calculate the distance
        dis = travel / 58;
        printf("%d\n",dis);
        delay(100);
        }
}


