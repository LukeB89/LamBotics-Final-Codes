#include "FastLED.h"
#include "String.h"

// How many leds in your strip?
#define NUM_LEDS 16

// For led chips like Neopixels, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
#define DATA_PIN 3
//#define CLOCK_PIN 13

// Define the array of leds
CRGB leds[NUM_LEDS];
char* color;
char incomingByte[11];   // for incoming serial data

void setup() 
{ 
      // starts the serial connection and sets baud rate
      Serial.begin(57600);
      // sets up the NeoPixle code
      FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
      
    
}

void loop() 
{ 
// checks for incomming on the serial port
if (Serial.available() > 0) 
{
  inc = 0;
  // read the incoming byte:
  Serial.readBytes(incomingByte,11);
  // stores the first part of the incoming data up to the seporator
  // denoted by ":"
  char* command = strtok(incomingByte, ":");
  while (command != 0)
  {
    //stores the command into color
    color = command;//atoi(command);
    // seraches for the next ":" and exits loop when not found
    command = strtok(0,":");

  }
  

  
  // displays the result:
  Serial.print("R: ");
  Serial.println(color);
}
// Sets brightness on LED's
FastLED.setBrightness(255);

// Starts loop from 0 to 15 (16 LED's)
for (int x = 0; x < NUM_LEDS; x++)
{
  // Applies HEX to each LED in the sequence
  leds[x] = strtoul(color, NULL, 16);
}
// in forms LED's to display color. 
FastLED.show();    
}
  
  

