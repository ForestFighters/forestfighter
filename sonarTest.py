import RPi.GPIO as GPIO, sys, threading, time

#use physical pin numbering
GPIO.setmode(GPIO.BOARD)

#set up digital line detectors as inputs
GPIO.setup(12, GPIO.IN)
GPIO.setup(13, GPIO.IN)

#use pwm on inputs so motors don't go too fast
GPIO.setup(19, GPIO.OUT)
p=GPIO.PWM(19, 20)
p.start(0)
GPIO.setup(21, GPIO.OUT)
q=GPIO.PWM(21, 20)
q.start(0)
GPIO.setup(24, GPIO.OUT)
a=GPIO.PWM(24,20)
a.start(0)
GPIO.setup(26, GPIO.OUT)
b=GPIO.PWM(26,20)
b.start(0)

# Setup LED pins as outputs
LED1 = 22
LED2 = 18
LED3 = 11
LED4 = 07
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

def setLEDs(L1, L2, L3, L4):
  GPIO.output(LED1, L1)
  GPIO.output(LED2, L2)
  GPIO.output(LED3, L3)
  GPIO.output(LED4, L4)

setLEDs(1, 1, 1, 1)

# Define Sonar Pin for Trigger and Echo to be the same
SONAR = 8

try:
   while True:
       GPIO.setup(SONAR, GPIO.OUT)
       GPIO.output(SONAR, True)
       time.sleep(0.00001)
       GPIO.output(SONAR, False)
       start = time.time()
       count = time.time()
       GPIO.setup(SONAR, GPIO.IN)
       while GPIO.input(SONAR)==0 and time.time()-count<0.1:
           start = time.time()
       stop=time.time()
       while GPIO.input(SONAR)==1:
           stop = time.time()
       # Calculate pulse length
       elapsed = stop-start
       # Distance pulse travelled in that time is time
       # multiplied by the speed of sound (cm/s)
       distance = elapsed * 34000
       # That was the distance there and back so halve the value
       distance = distance / 2
       print 'Distance:', distance
       time.sleep(1)

except KeyboardInterrupt:
       GPIO.cleanup()

