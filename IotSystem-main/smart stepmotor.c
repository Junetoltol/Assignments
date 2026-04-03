#include <wiringPi.h>
#define PIN_1A 27
#define PIN_1B 0
#define PIN_2A 1
#define PIN_2B 24

int main(void){
        int i=0;
        if(wiringPiSetup() == -1) return 1;
        pinMode(PIN_1A,OUTPUT);
        pinMode(PIN_1B,OUTPUT);
        pinMode(PIN_2A,OUTPUT);
        pinMode(PIN_2B,OUTPUT);
        for(i=0;i<500;i++){
                digitalWrite(PIN_1A,HIGH);
                digitalWrite(PIN_1B,LOW);
                digitalWrite(PIN_2A,LOW);
                digitalWrite(PIN_2B,LOW);
                usleep(3)
                digitalWrite(PIN_1A,LOW);
                digitalWrite(PIN_1B,HIGH);
                digitalWrite(PIN_2A,LOW);
                digitalWrite(PIN_2B,LOW);
                usleep(3)
                digitalWrite(PIN_1A,LOW);
                digitalWrite(PIN_1B,LOW);
                digitalWrite(PIN_2A,HIGH);
                digitalWrite(PIM_2B,LOW);
                usleep(3)
                digitalWrite(PIN_1A,LOW);
                digitalWrite(PIN_1B,LOW);
                digitalWrite(PIN_2A,LOW);
                digitalWrite(PIN_2B,HIGH);
                usleep(3)
        }
}
