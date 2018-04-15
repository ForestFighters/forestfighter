import RPi.GPIO as GPIO
import sys, threading, time


class Sonar(object):
    def __init__(self):

        # Setup LED pins as outputs
        self.LED1 = 24
        self.SONAR = 14
        GPIO.setup(self.LED1, GPIO.OUT)

    def set_leds(self, L1):
        GPIO.output(self.LED1, L1)

    def get_distance(self):
        """Returns distance in cm"""
        self.set_leds(1)
        GPIO.setup(self.SONAR, GPIO.OUT)
        GPIO.output(self.SONAR, True)
        time.sleep(0.00001)
        GPIO.output(self.SONAR, False)
        start = time.time()
        count = time.time()
        GPIO.setup(self.SONAR, GPIO.IN)
        while GPIO.input(self.SONAR) == 0 and time.time() - count < 0.1:
            start = time.time()
        stop = time.time()
        while GPIO.input(self.SONAR) == 1:
            stop = time.time()
        # Calculate pulse length
        elapsed = stop - start
        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34000
        # That was the distance there and back so halve the value
        distance = distance / 2
        return distance