#include <wiringPi.h>
#include <stdio.h>
#define PIN 3

int main(void){
	int sw,i;
	
	if(wiringPiSetup() == -1){
		return 1;
		}
	pinMode(PIN,INPUT);

	for(i=0; i<10; i++){
		sw = digitalRead(PIN);
		printf("%d\n",sw);
		delay(100);
	}
}