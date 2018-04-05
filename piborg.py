#!/usr/bin/env python
# coding: Latin

# Load library functions we want
import time
import os
import sys
# import ThunderBorg
import io
import threading
import picamera
import picamera.array
import cv2
import numpy
from streamprocessor import StreamProcessor
from imagecapture import ImageCapture

print('Libraries loaded')

# Global values
global running
# global TB
global camera
global processor
global debug
global colour

running = True
debug = True
colour = 'blue'

# Setup the ThunderBorg
# TB = ThunderBorg.ThunderBorg()
# TB.i2cAddress = 0x15                  # Uncomment and change the value if you have changed the board address
# TB.Init()
##if not TB.foundChip:
##    boards = ThunderBorg.ScanForThunderBorg()
##    if len(boards) == 0:
##        print('No ThunderBorg found, check you are attached :)'
##    else:
##        print('No ThunderBorg at address %02X, but we did find boards:' % (TB.i2cAddress)
##        for board in boards:
##            print('    %02X (%d)' % (board, board)
##        print('If you need to change the IÃÂ²C address change the setup line so it is correct, e.g.'
##        print('TB.i2cAddress = 0x%02X' % (boards[0])
##    sys.exit()
##TB.SetCommsFailsafe(False)

# Power settings
##voltageIn = 12.0                        # Total battery voltage to the ThunderBorg
##voltageOut = 12.0 * 0.95                # Maximum motor voltage, we limit it to 95% to allow the RPi to get uninterrupted power

# Camera settings
imageWidth = 320  # Camera image width
imageHeight = 240  # Camera image height
frameRate = 3  # Camera image capture frame rate

# Auto drive settings
autoMaxPower = 1.0  # Maximum output in automatic mode
autoMinPower = 0.2  # Minimum output in automatic mode
autoMinArea = 10  # Smallest target to move towards
autoMaxArea = 10000  # Largest target to move towards
autoFullSpeedArea = 300  # Target size at which we use the maximum allowed output


# Setup the power limits
##if voltageOut > voltageIn:
##    maxPower = 1.0
##else:
##    maxPower = voltageOut / float(voltageIn)
##autoMaxPower *= maxPower


# Startup sequence
print('Setup camera')
camera = picamera.PiCamera()
camera.resolution = (imageWidth, imageHeight)
camera.framerate = frameRate
imageCentreX = imageWidth / 2.0
imageCentreY = imageHeight / 2.0

print('Setup the stream processing thread')
processor = StreamProcessor(camera)

print('Wait ...')
time.sleep(2)
captureThread = ImageCapture(camera, processor)

try:
    print('Press CTRL+C to quit')
    ##    TB.MotorsOff()
    ##    TB.SetLedShowBattery(True)
    # Loop indefinitely until we are no longer running
    while running:
        # Wait for the interval period
        # You could have the code do other work in here 🙂
        time.sleep(1.0)
        # Disable all drives
##    TB.MotorsOff()
except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    print('\nUser shutdown')
##    TB.MotorsOff()
except:
    # Unexpected error, shut down!
    e = sys.exc_info()[0]
    print
    print(e)
    print('\nUnexpected error, shutting down!')
##    TB.MotorsOff()
# Tell each thread to stop, and wait for them to end
running = False
captureThread.join()
processor.terminated = True
processor.join()
del camera
##TB.MotorsOff()
##TB.SetLedShowBattery(False)
##TB.SetLeds(0,0,0)
print('Program terminated.')