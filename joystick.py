import pygame
import os
import time
import logging
import sys


LOGGER = logging.getLogger(__name__)


class Joystick(object):
    def __init__(self, axis_up_down=1,
                 axis_up_down_inverted=False,
                 axis_left_right=2,
                 axis_left_right_inverted=False,
                 button_reset_epo=9,
                 button_slow=6,
                 slow_factor=0.5,
                 button_fast_turn=8):
        self.joystick = self.wait_on_joystick()
        self.joystick.init()
        self.axis_up_down = axis_up_down
        self.axis_up_down_inverted = axis_up_down_inverted
        self.axis_left_right = axis_left_right
        self.axis_left_right_inverted = axis_left_right_inverted
        self.button_reset_epo = button_reset_epo
        self.button_slow = button_slow
        self.slow_factor = slow_factor
        self.button_fast_turn = button_fast_turn

    def wait_on_joystick(self):
        joystick = None
        os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have a GUI window
        pygame.init()
        pygame.display.set_mode((1,1))
        LOGGER.info('Waiting for joystick... (press CTRL+C to abort)')
        while True:
            try:
                try:
                    pygame.joystick.init()
                    # Attempt to setup the joystick
                    if pygame.joystick.get_count() == 0:
                        # No joystick attached, toggle the LED
                        LOGGER.warn('No Joystick attached')
                        pygame.joystick.quit()
                        time.sleep(0.5)
                    else:
                        # We have a joystick, attempt to initialise it!
                        joystick = pygame.joystick.Joystick(0)
                        break
                except pygame.error:
                    # Failed to connect to the joystick, toggle the LED
                    LOGGER.error('Failled to connect to joystick')
                    pygame.joystick.quit()
                    time.sleep(0.5)
            except KeyboardInterrupt:
                # CTRL+C exit, give up
                LOGGER.info('\nUser aborted')
                sys.exit()

        LOGGER.info('Joystick found')
        return joystick

    def get_reading(self):
        # get the base reading
        up_down = self.joystick.get_axis(self.axis_up_down)
        left_right = self.joystick.get_axis(self.axis_left_right)

        # flip it if the axis are inverted
        if self.axis_up_down_inverted:
            up_down = -up_down
        if self.axis_left_right_inverted:
            left_right = -left_right

        # Apply steering speeds
        if not self.joystick.get_button(self.button_fast_turn):
            left_right *= 0.5

        drive_left = -up_down
        drive_right = -up_down
        if left_right < -0.05:
            # Turning left
            drive_left *= 1.0 + (2.0 * left_right)
        elif left_right > 0.05:
            # Turning right
            drive_right *= 1.0 - (2.0 * left_right)
        # Check for button presses
        if self.joystick.get_button(self.button_reset_epo):
            LOGGER.debug('reset')
        if self.joystick.get_button(self.button_slow):
            drive_left *= self.slow_factor
            drive_right *= self.slow_factor


        if self.joystick.get_button(self.button_slow):
            drive_left *= self.slow_factor
            drive_right *= self.slow_factor

        return drive_left, drive_left