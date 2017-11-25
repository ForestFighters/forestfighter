from gpiozero import LED
from gpiozero import Robot

from time import sleep

ENABLE_LEFT=17
LEFT_A=18
LEFT_B=27

ENABLE_RIGHT=22
RIGHT_A=23
RIGHT_B=24

# Not actually LEDs, but we need to turn them on and off

left_enable = LED(ENABLE_LEFT)
right_enable = LED(ENABLE_RIGHT)

# Power up!

left_enable.on ()
right_enable.on ()

# Let's motor (see what I did there?)

robot = Robot (left=(LEFT_B, LEFT_A), right=(RIGHT_A, RIGHT_B))

print ("Full steam reverse!")

robot.backward ()
sleep (1)

print ("Stop")

robot.stop ()
sleep (1)

print ("Full steam ahead!")

robot.forward ()
sleep (1)

print ("Stop")

robot.stop ()
sleep (1)

print ("Turn right")

robot.right ()
sleep (1)

print ("Stop")

robot.stop ()
sleep (1)

print ("Turn left")

robot.left ()
sleep (1)

print ("Stop")

robot.stop ()
sleep (1)

print ("Full steam reverse!")

robot.backward ()
sleep (1)

print ("Stop")

robot.stop ()
sleep (1)

# Power down

left_enable.off ()
right_enable.off ()


