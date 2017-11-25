#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import os
import sys
import pygame
#import EdBot
from gpiozero import LED
from gpiozero import Motor

ENABLE_LEFT=17
LEFT_A=18
LEFT_B=27

ENABLE_RIGHT=22
RIGHT_A=23
RIGHT_B=24

# prepare left and right

left_enable = LED(ENABLE_LEFT)
right_enable = LED(ENABLE_RIGHT)

left_enable.off()
right_enable.off()

# Create motor controllers

left_motor  = Motor ( LEFT_A,  LEFT_B)
right_motor = Motor (RIGHT_A, RIGHT_B)

# All stop!

left_motor.stop ()
right_motor.stop ()

# Enable motors

left_enable.on()
right_enable.on()

left_motor.forward ()
right_motor.forward ()

time.sleep (5)
sys.exit (0)

# Set variables for the GPIO motor pins
# pinMotorAForwards = 18
# pinMotorABackwards = 27
# pinMotorBForwards = 23
# pinMotorBBackwards = 24

# LeftMotor = EdBot.motor.one
# RightMotor = EdBot.motor.two

# Re-direct our output to standard error, we need to ignore standard out to hide some nasty print statements from pygame
sys.stdout = sys.stderr

# Settings for the joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 2                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
buttonResetEpo = 9                      # Joystick button number to perform an EPO reset (Start)
buttonSlow = 6                          # Joystick button number for driving slowly whilst held (L2)
slowFactor = 0.5                        # Speed to slow to when the drive slowly button is held, e.g. 0.5 would be half speed
buttonFastTurn = 7                      # Joystick button number for turning fast (R2)
interval = 0.00                         # Time between updates in seconds, smaller responds faster but uses more processor time

# Power settings
voltageIn = 6.0                        # Total battery voltage to the PicoBorg Reverse
voltageOut = 5.0 #* 0.95                # Maximum motor voltage, we limit it to 95% to allow the RPi to get uninterrupted power

# Setup the power limits
if voltageOut > voltageIn:
    maxPower = 1.0
else:
    maxPower = voltageOut / float(voltageIn)

# Setup pygame and wait for the joystick to become available
#EdBot.motor.speed(0)
os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have a GUI window
pygame.init()
pygame.display.set_mode((1,1))
print 'Waiting for joystick... (press CTRL+C to abort)'
while True:
    try:
        try:
            pygame.joystick.init()
            # Attempt to setup the joystick
            if pygame.joystick.get_count() == 0:
                # No joystick attached, toggle the LED
                print('No Joystick attached')
                pygame.joystick.quit()
                time.sleep(0.5)
            else:
                # We have a joystick, attempt to initialise it!
                joystick = pygame.joystick.Joystick(0)
                break
        except pygame.error:
            # Failed to connect to the joystick, toggle the LED
            print('Failled to connect to joystick')
            pygame.joystick.quit()
            time.sleep(0.5)
    except KeyboardInterrupt:
        # CTRL+C exit, give up
        print '\nUser aborted'

        sys.exit()
print 'Joystick found'
joystick.init()


try:
    print 'Press CTRL+C to quit'
    driveLeft = 0.0
    driveRight = 0.0
    running = True
    hadEvent = False
    upDown = 0.0
    leftRight = 0.0
    # Loop indefinitely
    while running:
        # Get the latest events from the system
        hadEvent = False
        events = pygame.event.get()
        # Handle each event individually
        for event in events:
            if event.type == pygame.QUIT:
                # User exit
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                # A button on the joystick just got pushed down
                hadEvent = True
            elif event.type == pygame.JOYAXISMOTION:
                # A joystick has been moved
                hadEvent = True
            if hadEvent:
                # Read axis positions (-1 to +1)
                if axisUpDownInverted:
                    upDown = -joystick.get_axis(axisUpDown)
                else:
                    upDown = joystick.get_axis(axisUpDown)
                if axisLeftRightInverted:
                    leftRight = -joystick.get_axis(axisLeftRight)
                else:
                    leftRight = joystick.get_axis(axisLeftRight)
                # Apply steering speeds
                if not joystick.get_button(buttonFastTurn):
                    leftRight *= 0.5
                # Determine the drive power levels
                driveLeft = -upDown
                driveRight = -upDown
                if leftRight < -0.05:
                    # Turning left
                    driveLeft *= 1.0 + (2.0 * leftRight)
                elif leftRight > 0.05:
                    # Turning right
                    driveRight *= 1.0 - (2.0 * leftRight)
                # Check for button presses
                if joystick.get_button(buttonResetEpo):
                    print('reset')
                if joystick.get_button(buttonSlow):
                    driveLeft *= slowFactor
                    driveRight *= slowFactor
                # Set the motors to the new speeds
		print ("Left {}, right {}".format(driveLeft, driveRight))
                if driveLeft >= 0:
                    left_motor.forward (driveLeft)
                else:
                    left_motor.backward (-driveLeft)
                if driveRight >= 0:
                    right_motor.backward (driveRight)
                else:
                    right_motor.forward (-driveRight)
                    
                #LeftMotor.speed((driveRight * maxPower)*100)
                #RightMotor.speed((-driveLeft * maxPower)*100)
        # Change the LED to reflect the status of the EPO latch
        #PBR.SetLed(PBR.GetEpo())
        # Wait for the interval period
        time.sleep(interval)
    # Disable all drives
    #LeftMotor.speed(0)
    #RightMotor.speed(0)
except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    #LeftMotor.speed(0)
    #RightMotor.speed(0)
    print ('Motors off')
