#include <wiringPi.h>
#define PIN_INA 26
#define PIN_INB 23

int main(void){
	if(wiringPiSetup() == -1){
	return 1;
	}

	pinMode(PIN_INA,OUTPUT);
	pinMode(PIN_INB,OUTPUT);

	digitalWrite(PIN_INA,HIGH);
	delay(3000);
	digitalWrite(PIN_INA,LOW);
	digitalWrite(PIN_INB,HIGH);
	delay(3000);
	digitalWrite(PIN_INB,LOW);
}