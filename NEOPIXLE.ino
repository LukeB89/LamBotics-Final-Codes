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
      Serial.begin(57600);
      FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
      
    
}

void loop() 
{ 
if (Serial.available() > 0) 
{
  inc = 0;
  // read the incoming byte:
  Serial.readBytes(incomingByte,11);
  char* command = strtok(incomingByte, ":");
  while (command != 0)
  {
    color = command;//atoi(command);
    command = strtok(0,":");

  }
  

  
  // say what you got:
  Serial.print("R: ");
  Serial.println(color);
}
//Serial.readBytes(11
FastLED.setBrightness(255);

for (int x = 0; x < NUM_LEDS; x++)
{
  leds[x] = strtoul(color, NULL, 16);
}

FastLED.show();    
}
  
  

