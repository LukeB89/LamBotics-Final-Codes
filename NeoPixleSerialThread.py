#!/usr/bin/python
import DynamicObjectV2
import webcolors
import os.path
import serial
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
Obj = DynamicObjectV2.Class

ser = serial.Serial("/dev/ttyUSB0",57600)
time.sleep(3)

# put your imports here
## Obtains the name of the closest color based on RGB values 
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def sendMSG(Red,Gre,Blu):
    ## creats array of the RGB values
    requested_colour = (Red, Gre, Blu)
    ## Sends array to obtain the closest Web Colour Name
    closest_name = closest_colour(requested_colour)
    ## Converts Colour Name to Hex
    Hex = webcolors.name_to_hex(closest_name).encode('ascii','ignore')
    # Used in testing
##  HexV = ColrDTC.Hex
##  Hex = "%s" %HexV
##    self.message(Hex)
##    Hex = "#101010"
    # Extracts what is needed
    inpu = Hex[1:]
    # Writes to serial
    ser.write('%s' %(Hex[1:]))
    # Used in testing
##    ser.write('ff0000')
    time.sleep(1)
    return inpu

## Alters the scale of the x, y and z values
## To make them in the range of 0 -255
## To mimic the RGB values to send to the 
## Arduino
def facePosScale(a,b,c):    
    reX = int(round((a*2.125)))
    reY = int(round((b*2.742)))
    reZ = int(round(((c-50)*2.55)))
    reP = (reX,reY,reZ)
    return reP




def init(self):
    # put your self.registerOutput here
    self.registerOutput("NeoPixle", Obj("Send", False))

def run (self):

    # main loop
    while 1:
        # put your logic here
        x = 0
        color = (0,0,0)
        # you can use: output, getInputs, message
        ## Gets message inputs from color detection
        ## And face detection threads
        ColrDTC = self.getInputs().colourDTC
        HeadP = self.getInputs().facePos
        FaceD = self.getInputs().faceDet
        ## Ensures only Color detect module or face
        ## Detect module has control of sending serial commands at any one time.
        if(ColrDTC.Working == True):
            ## Uses Send Message controls to send RGB values 
            ## To that of the NeoPixle Code upon the Arduino 
            sendMSG(ColrDTC.R, ColrDTC.G, ColrDTC.B)
            ## Comment in for testing
##          self.message(x)
        elif(FaceD.Face == True):
            ## First converts x, y and z values to range of 
            ## 0 - 255 then sends as RGB values to arduino
            ## To display on NeoPixles
            color = facePosScale(HeadP.x,HeadP.y,HeadP.z)
            
            x = sendMSG(color[0], color[1], color[2])
##            x = sendMSG(1, 1, 1)
            ## Comment in for testing
##          self.message(x)

       
        time.sleep(0.1)
