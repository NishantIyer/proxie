

#include "Arduino.h"
#include "Mic.h"
#include "SpeakerStereo3W.h"


#define MIC_3V3_PIN_SIG	12
#define STEREOSPEAKER_PIN_POS	0




unsigned int StereoSpeakerHoorayLength          = 6;                                                      // amount of notes in melody
unsigned int StereoSpeakerHoorayMelody[]        = {NOTE_C4, NOTE_E4, NOTE_G4, NOTE_C5, NOTE_G4, NOTE_C5}; // list of notes. List length must match HoorayLength!
unsigned int StereoSpeakerHoorayNoteDurations[] = {8      , 8      , 8      , 4      , 8      , 4      }; // note durations; 4 = quarter note, 8 = eighth note, etc. List length must match HoorayLength!
// object initialization
Mic mic_3v3(MIC_3V3_PIN_SIG);
SpeakerStereo3W StereoSpeaker(STEREOSPEAKER_PIN_POS);


// define vars for testing menu
const int timeout = 10000;       //define timeout of 10 sec
char menuOption = 0;
long time0;

// Setup the essentials for your circuit to work. It runs first every time your circuit is powered with electricity.
void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(9600);
    while (!Serial) ; // wait for serial port to connect. Needed for native USB
    Serial.println("start");
    
    
    menuOption = menu();
    
}

void loop() 
{
    
    
    if(menuOption == '1') {
    // Electret Microphone Breakout - Test Code
    int mic_3v3Val = mic_3v3.read();
    Serial.print(F("Val: ")); Serial.println(mic_3v3Val);

    }
    else if(menuOption == '2') {
    // 3W Stereo Speaker - Test Code
    // The Speaker will play the Hooray tune
    StereoSpeaker.playMelody(StereoSpeakerHoorayLength, StereoSpeakerHoorayMelody, StereoSpeakerHoorayNoteDurations); 
    delay(500);   
    }
    
    if (millis() - time0 > timeout)
    {
        menuOption = menu();
    }
    
}




char menu()
{

    Serial.println(F("\nWhich component would you like to test?"));
    Serial.println(F("(1) Electret Microphone Breakout"));
    Serial.println(F("(2) 3W Stereo Speaker"));
    Serial.println(F("(menu) send anything else or press on board reset button\n"));
    while (!Serial.available());

    // Read data from serial monitor if received
    while (Serial.available()) 
    {
        char c = Serial.read();
        if (isAlphaNumeric(c)) 
        {   
            
            if(c == '1') 
    			Serial.println(F("Now Testing Electret Microphone Breakout"));
    		else if(c == '2') 
    			Serial.println(F("Now Testing 3W Stereo Speaker"));
            else
            {
                Serial.println(F("illegal input!"));
                return 0;
            }
            time0 = millis();
            return c;
        }
    }
}
