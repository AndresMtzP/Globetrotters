#include <iostream>
#include <fstream>
#include <wiringPiI2C.h>
#include <string.h>
#include "APDS9960_RPi.h"

using namespace std;

// Compile: g++ -o GestInput GestInput.cpp APDS9960_RPi.cpp -lwiringPi
// Load I2C: gpio load i2c
// Run: ./gestsensor

// Pins
#define APDS9960_INT 7
#define LED_DELAY 800	// time to toggle LED color
#define LED_LEFT 4		//pin 16
#define LED_RIGHT 	5	//pin 18
#define LED_UP 	6		//pin 22
#define LED_DOWN 10		//pin 24
#define LED_MIC 11
#define LED_SELECT 51	// Select & Stop toggles all LEDs
#define LED_STOP 52
#define ON 1			// Toggles LEDs on/off
#define OFF 0

// Global Variables
APDS9960_RPi apds = APDS9960_RPi();
int isr_flag = 0;
int seqNum = 9;

/* function declarations
void interruptRoutine();
void handleGesture();
void GUICom3(char* GUICmd);
void togLED(int LED);
void testLED(int LED);
*/

int main() {
	// Test LEDs
	testLED(LED_UP);
	testLED(LED_DOWN);
	testLED(LED_LEFT);
	testLED(LED_RIGHT);
	testLED(LED_MIC);


	// init wiringPi
	wiringPiSetup();

	// Initialize interrupt service routine
	wiringPiISR(APDS9960_INT, INT_EDGE_FALLING,  interruptRoutine);

	// Initialize APDS-9960 (configure I2C and initial values)
	if ( apds.init() ) {
		cout << "APDS-9960 init complete" << endl;
	} else {
		cout << "APDS-9960 init failed" << endl;
	}

	// Start running the APDS-9960 gesture sensor engine
	if ( apds.enableGestureSensor(true) ) {
		cout << "Gesture sensor enabled" << endl;
	} else {
		cout << "Gesture sensor failed to execute" << endl;
	}

	while(1) {
		if( isr_flag == 1 ) {
			handleGesture();
			isr_flag = 0;
		}
	}
	return 0;
}



void interruptRoutine() {
	isr_flag = 1;
}



void handleGesture() {
	char zoomIn[] = "zoomIn";
	char zoomOut[] = "zoomOut";
	char swipeL[] = "swipeL";
	char swipeR[] = "swipeR";
	char stop[] = "stop";
	char selectItem[] = "selectItem";
	
	if ( apds.isGestureAvailable() ) {
		switch ( apds.readGesture() ) {
		case DIR_UP:
			GUICom3(zoomOut);
			togLED(LED_UP);
			break;
		case DIR_DOWN:
			GUICom3(zoomIn);
			togLED(LED_DOWN);
			break;
		case DIR_LEFT:
			GUICom3(swipeL);
			togLED(LED_LEFT);
			break;
		case DIR_RIGHT:
			GUICom3(swipeR);
			togLED(LED_RIGHT);
			break;
		case DIR_NEAR:
			GUICom3(selectItem);
			togLED(LED_SELECT);
			break;
		case DIR_FAR:
			GUICom3(stop);
			togLED(LED_STOP);
			break;
		default:
			cout << "GestInput: undetermined" << endl;
		}
	}
	else {
		cout << "GestInput: No gesture" << endl;
	}
}




void GUICom3(char* GUICmd) {
	seqNum = ((seqNum + 1) % 3) + 9;
	cout << "GestInput: " << GUICmd << ". Sequence# " << seqNum << endl;
	ofstream cmdFile;

	// Handle globe commands: swipel, swiper, stop
	// strcmp() returns 0 if strings are equal
	if(strcmp(GUICmd, "swipeL") == 0 || strcmp(GUICmd, "swipeR") == 0 || strcmp(GUICmd, "stop") == 0) {
		cmdFile.open ("/home/pi/globe/Rotation/commands");
  		cmdFile << GUICmd;
	}
	else {
	// Handle GUI commands: zoomIn/down, zoomOut/up, selectItem
  	cmdFile.open ("/var/www/html/GUICom.json");
  	cmdFile << "{\"SeqNum\": " << seqNum << ", \"GUICommand\": \"" << GUICmd << "\"}";
  	}
  	cmdFile.close();
}



void togLED(int LED) {
	// toggles LED based on gesture input
	if(LED == LED_SELECT || LED == LED_STOP) {
		pinMode (LED_LEFT, OUTPUT);
		pinMode (LED_RIGHT, OUTPUT);
		pinMode (LED_UP, OUTPUT);
		pinMode (LED_DOWN, OUTPUT);
	  	digitalWrite (LED_LEFT, ON);
	  	digitalWrite (LED_RIGHT, ON);
	  	digitalWrite (LED_UP, ON);
	  	digitalWrite (LED_DOWN, ON);
	  	delay (LED_DELAY);
	  	digitalWrite (LED_LEFT, OFF);
	  	digitalWrite (LED_RIGHT, OFF);
	  	digitalWrite (LED_UP, OFF);
	  	digitalWrite (LED_DOWN, OFF);
	}
	else {
		pinMode (LED, OUTPUT);
	  	digitalWrite (LED, ON);
	  	delay (LED_DELAY);
	  	digitalWrite (LED, OFF);
	}
}


void testLED(int LED) {
	pinMode (LED, OUTPUT);
  	digitalWrite (LED, ON);
  	delay (1600);
  	digitalWrite (LED, OFF);

}


















