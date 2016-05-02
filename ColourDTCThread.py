#!/usr/bin/python
from picamera.array import PiRGBArray
from matplotlib import pyplot as plt
from picamera import PiCamera
import DynamicObjectV2
import numpy as np
import webcolors
import os.path
import time
import cv2
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
Obj = DynamicObjectV2.Class

widths = 440
heigths = 280

resX = 6
resY = 6
count = 0
imc = 0

hue = 0
sat = 0
val = 0
camera = PiCamera()
camera.resolution = (widths, heigths)
camera.framerate = 32
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(widths, heigths))

time.sleep(0.1)

def dec_conv(x):
    return format(x, '03d')

def init(self):
    # put your self.registerOutput here
    self.registerOutput("colourDTC", Obj("R",0,"G",0,"B",0,"NewColor",True,"Working", False))

def run (self):
    # put your init and global variables here
    
    # main loop
    while 1:
        oldRGB = [0,0,0]
        newRGB = [0,0,0]
            # capture frames from the camera
        for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                frame = image.array
                size = 20
                mag = 0.5
                x = (widths/2)- size
                y = (heigths/2) - size
                w = (widths/2) + size

                # Sets up the Image for processing and display
                blr = cv2.blur(frame,(10,10))
                cv2.rectangle(frame,(x,y),(w,h),(255,0,0),1)
                cv2.line(frame, (x,y),(w,h),(255,0,0),1)
                cv2.line(frame, (x,h),(w,y),(255,0,0),1)
                cv2.circle(frame, (220, 140),2,(0,255,0),2)

                # Masks an area such that the colour dectection only views
                # A small section of the screen
                maskd = np.zeros(blr.shape[:2], np.uint8)
                maskd[130:150, 210:230] = 255
                # Applies the mask to the image, Calculates the mean of area
                # returns three values, Red, Green and Blue
                con = cv2.mean(blr,mask = maskd)
                Red = int(con[2])
                Gre = int(con[1])
                Blu = int(con[0])
                #Displaying Values
                cv2.putText(frame,"Red=(%r)" % Red, (1,20), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)
                cv2.putText(frame,"Green=(%r)" % Gre, (widths/3,20), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)
                cv2.putText(frame,"Blue=(%r)" % Blu, (2*widths/3,20), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)
                # Control to stop repeat sending
                newRGB = [Red,Gre,Blu]
                if(newRGB != oldRGB):
                    oldRGB = newRGB
                    self.output("colourDTC",Obj("R",None,"G",None,"B",None,"NewColour",False,"Working", True))
                    self.output("colourDTC",Obj("R",Red,"G",Gre,"B",Blu,"NewColour",True,"Working",True))


                #Displaying the image
                cv2.imwrite("save.png", frame)
                new = cv2.imread("save.png")
                cv2.imshow('frame', new)
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)

                
                # Check for keypresses
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print "Q Pressed"
                    break
                

        print "Quitting..."
        '''cam.release()'''
        break
        cv2.destroyAllWindows()
