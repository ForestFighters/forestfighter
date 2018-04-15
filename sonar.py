import RPi.GPIO as GPIO
import sys, threading, time


class Sonar(object):
    def __init__(self):
        # use physical pin numbering
        GPIO.setmode(GPIO.BOARD)

        # set up digital line detectors as inputs
        GPIO.setup(12, GPIO.IN)
        GPIO.setup(13, GPIO.IN)

        # use pwm on inputs so motors don't go too fast
        GPIO.setup(19, GPIO.OUT)
        p = GPIO.PWM(19, 20)
        p.start(0)
        GPIO.setup(21, GPIO.OUT)
        q = GPIO.PWM(21, 20)
        q.start(0)
        GPIO.setup(24, GPIO.OUT)
        a = GPIO.PWM(24, 20)
        a.start(0)
        GPIO.setup(26, GPIO.OUT)
        b = GPIO.PWM(26, 20)
        b.start(0)

        # Setup LED pins as outputs
        self.LED1 = 22
        self.LED2 = 18
        self.LED3 = 11
        self.LED4 = 7
        self.SONAR = 8
        GPIO.setup(self.LED1, GPIO.OUT)
        GPIO.setup(self.LED2, GPIO.OUT)
        GPIO.setup(self.LED3, GPIO.OUT)
        GPIO.setup(self.LED4, GPIO.OUT)

    def set_leds(self, L1, L2, L3, L4):
        GPIO.output(self.LED1, L1)
        GPIO.output(self.LED2, L2)
        GPIO.output(self.LED3, L3)
        GPIO.output(self.LED4, L4)

    def get_distance(self):
        """Returns distance in cm"""
        self.set_leds(1, 1, 1, 1)
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