#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import sys
import pygame
from robot import AmyBot, CamJamBot, FourTronix
from joystick import Joystick
from argparse import ArgumentParser
import logging
from time import sleep
from rainbow import Rainbow
import grove_oled
from sonar import Sonar


L1_BUTTON = 6  # L1 rainbow
L2_BUTTON = 8  # R1 remote
R1_BUTTON = 7  # L2 maze
R2_BUTTON = 9  # R2 straight
INTERVAL = 0.0


LOGGER = logging.getLogger(__name__)


class Controller(Rainbow, Sonar):
    mode = R1_BUTTON

    def __init__(self, amybot=True, cambot=False, fourtronix=False, straight=False):
        Sonar.__init__(self)
        Rainbow.__init__(self)
        print ("Hello!")
        self.last_text = "Bleurgh!"
        self.joystick = Joystick()
        # if elsing this because the init methods of both classes do stuff with hardware, so best to only intiailise deliberately
        if amybot:
            self.bot = AmyBot()
            LOGGER.info('Enable AmyBot')
        elif cambot:
            self.bot = CamJamBot()
            LOGGER.info('Enable CamJamBot')
        elif fourtronix:
            self.bot = FourTronix()
            LOGGER.info('Enable FourTronixBot')
        else:
            print("Unknown Robot Type")
            sys.exit(0)
        self.straight = True
        if self.straight:
            self.mode = R2_BUTTON

        # Re-direct our output to standard error, we need to ignore standard out to hide some nasty print statements from pygame
        sys.stdout = sys.stderr

        interval = 0.0

        self.straight_line_start = False
        self.modes = {L1_BUTTON: self.rainbow, R1_BUTTON: self.remote, L2_BUTTON: self.maze, R2_BUTTON: self.straight}
        super().__init__()

    def run(self):
        grove_oled.oled_init()
        grove_oled.oled_clearDisplay()
        grove_oled.oled_setNormalDisplay()
        grove_oled.oled_setVerticalMode()
        self.show ("Amybot!")
        
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
                        if event.button == R2_BUTTON:
                            self.straight_line_start = not self.straight_line_start
                try:
                    self.modes[self.mode]()
                except KeyError:
                    LOGGER.warning("No mode set for key %i", self.mode)
                    self.mode = R1_BUTTON
                time.sleep(INTERVAL)

        except KeyboardInterrupt:
            # CTRL+C exit, disable all drives
            self.bot.move(0, 0)
            self.show('Motors off')

    def remote(self):
        self.show("Remote mode")
        left_drive, right_drive = self.joystick.get_reading()
        self.bot.move(left_drive, right_drive)

    def maze(self):
        self.show("Maze mode")

    def adjust_power(self, power, gap):
        return (power - (gap / 100))

    def straight(self):
        self.show("Line mode")
        left_power = 1.0
        right_power = 1.0
        while self.straight_line_start:
            try:
                dist = self.get_distance()
                if (dist < 80):
                    left_power = self.adjust_power(left_power, 80 - dist)
                elif (dist > 100):
                    right_power = self.adjust_power(right_power, 100 - dist)
                else:
                    left_power = 1.0
                    right_power = 1.0

                sleep(0.1)
                print(left_power, right_power)
                self.bot.move(left_power, right_power)

            except TypeError:
                print("Type Error")
            except IOError:
                print("IO Error")
        self.bot.stop()

    def show(self, text):
        LOGGER.debug(text)

        if text != self.last_text:
            #grove_oled.oled_clearDisplay()
            grove_oled.oled_setTextXY(0,0)
            grove_oled.oled_putString(text.center(12))
            self.last_text = text



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser()
    # either fortronix, amybot or camjambot can be passed in, but only one
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--amybot", help="Use the kit amy has (whatever Jim provided)", action="store_true")
    group.add_argument("--camjambot", help="Use the camjam edubot kit", action="store_true")    
    group.add_argument("--fourtronix", help="Use the 4tronix controller", action="store_true")
    parser.add_argument("--straight", help="go straight into straight line mode on start", action="store_true")
    args = parser.parse_args()

    controller = Controller(args.amybot, args.camjambot, args.fourtronix, args.straight)
    controller.run()
