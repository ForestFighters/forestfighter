#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import sys
import pygame
from robot import AmyBot, CamJamBot
from joystick import Joystick
from argparse import ArgumentParser
import logging

L1_BUTTON = 6
L2_BUTTON = 8
R1_BUTTON = 7
R2_BUTTON = 9
INTERVAL = 0.0


LOGGER = logging.getLogger(__name__)


class Controller(object):
    MODE = R1_BUTTON

    def __init__(self, cambot=False, amybot=True):
        self.joystick = Joystick()
        # if elsing this because the init methods of both classes do stuff with hardware, so best to only intiailise deliberately
        if amybot:
            self.bot = AmyBot()
        else:
            self.bot = CamJamBot()

        # Re-direct our output to standard error, we need to ignore standard out to hide some nasty print statements from pygame
        sys.stdout = sys.stderr

        interval = 0.0

        # Power settings
        voltage_in = 6.0  # Total battery voltage to the PicoBorg Reverse
        voltage_out = 5.0  # * 0.95                # Maximum motor voltage, we limit it to 95% to allow the RPi to get uninterrupted power

        # Setup the power limits
        if voltage_out > voltage_in:
            max_power = 1.0
        else:
            max_power = voltage_out / float(voltage_in)

        self.modes = {L1_BUTTON: self.rainbow, R1_BUTTON: self.remote, L2_BUTTON: self.maze, R2_BUTTON: self.follow}

    def run(self):
        try:
            LOGGER.info('Press CTRL+C to quit')
            running = True
            # Loop indefinitely
            while running:
                # Get the latest events from the system
                had_event = False
                events = pygame.event.get()
                # Handle each event individually
                for event in events:
                    if event.type == pygame.QUIT:
                        # User exit
                        running = False
                        break
                    elif event.type == pygame.JOYBUTTONDOWN:
                        # A button on the joystick just got pushed down
                        self.mode = event.button
                    self.modes[self.mode]()
                time.sleep(INTERVAL)

        except KeyboardInterrupt:
            # CTRL+C exit, disable all drives
            # LeftMotor.speed(0)
            # RightMotor.speed(0)
            LOGGER.debug('Motors off')

    def rainbow(self):
        pass

    def remote(self):
        left_drive, right_drive = self.joystick.get_reading()
        self.bot.move(left_drive, right_drive)

    def maze(self):
        pass

    def follow(self):
        pass



if __name__ == '__main__':
    parser = ArgumentParser()
    # either amybot or camjambot can be passed in, but not both.
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--amybot", help="Use the kit amy has (whatever Jim provided)", action="store_true")
    group.add_argument("--camjambot", help="Use the camjam edubot kit", action="store_true")
    args = parser.parse_args()

    controller = Controller(args.amybot, args.camjambot)
    controller.run()