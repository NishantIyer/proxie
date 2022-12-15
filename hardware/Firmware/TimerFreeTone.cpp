#include "TimerFreeTone.h"

uint8_t _tft_volume[] = { 255, 200, 150, 125, 100, 87, 50, 33, 22, 2 };      

void TimerFreeTone(uint8_t pin, unsigned long frequency, unsigned int duration, uint8_t volume) {
	if (frequency == 0 || volume == 0) {            
		delay(duration);
		return;
	} 
	frequency = 1000000 / frequency;                                     
	uint32_t duty = frequency / _tft_volume[min(volume, 10) - 1];      
#ifdef __AVR__
	uint8_t pinBit = digitalPinToBitMask(pin);                                        
	volatile uint8_t *pinOutput = (uint8_t *) portOutputRegister(digitalPinToPort(pin));        
	volatile uint8_t *portMode = (uint8_t *) portModeRegister(digitalPinToPort(pin));            
	*portMode |= pinBit;                                                             
#else
	pinMode(pin, OUTPUT);                                                            
#endif

	uint32_t startTime = millis();               
	while(millis() - startTime < duration) {     
	#ifdef __AVR__
		*pinOutput |= pinBit;       
		delayMicroseconds(duty);          
		*pinOutput &= ~pinBit;      
	#else
		digitalWrite(pin,HIGH);     
		delayMicroseconds(duty);          
		digitalWrite(pin,LOW);      
	#endif
		delayMicroseconds(frequency - duty);          
	}
}
