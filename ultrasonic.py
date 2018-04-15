#!/usr/bin/env python
#
# GrovePi Example for using the Grove Ultrasonic Ranger (http://www.seeedstudio.com/wiki/Grove_-_Ultrasonic_Ranger)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import grovepi
import time
import sys
from robot import FourTronix
import logging

def adjust_power(power, gap):
    return(power - (gap / 100))
    
    

def main():
    # Blue led on D4
    led = 4
    grovepi.pinMode(led,"OUTPUT")
    # Right sensor D8, Left sensor D7, Middle sensor D5
    # SIG,NC,VCC,GND
    ranger = 8
    left_power = 1.0
    right_power = 1.0

    bot = FourTronix()
    
    ledOn = 1
    starttime=time.time()
    while True:
        try:            
            if ledOn == 1 and time.time() - starttime > 1.0:
                ledOn = 0
                starttime = time.time()
            elif ledOn == 0 and time.time() - starttime > 1.0:
                ledOn = 1
                starttime = time.time()
				
            grovepi.digitalWrite(led,ledOn)
            print("Version: ", grovepi.version())
            # Read distance value from Ultrasonic
            dist = grovepi.ultrasonicRead(ranger)
            print("dist: ",dist)
            if( dist < 80 ):
                left_power = adjust_power(left_power, 80 - dist )
            elif( dist > 100 ):
                right_power = adjust_power(right_power, 100 - dist )
            else:
                left_power = 1.0
                right_power = 1.0
                
            sleep(0.1)
            print( left_power, right_power )
            bot.move(left_power, right_power)                

        except TypeError:
            print ("Type Error")
        except IOError:
            print ("IO Error")
        
        
if __name__ == '__main__':
    main()
