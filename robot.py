from gpiozero import Motor, LED
import logging


LOGGER = logging.getLogger(__name__)

class Robot(object):
    """
    Lowest possible abstraction of our robots.
    """
    def __init__(self, left_a_pin, left_b_pin, right_a_pin, right_b_pin):
        self.left_a_pin = left_a_pin
        self.left_b_pin = left_b_pin
        self.right_a_pin = right_a_pin
        self.right_b_pin = right_b_pin
        self.left_motor = Motor(self.left_a_pin, self.left_b_pin, pwm=True)
        self.right_motor = Motor(self.right_a_pin, self.right_b_pin, pwm=True)
        self.left_motor.stop()
        self.right_motor.stop()

    def move(self, left_drive, right_drive):
        LOGGER.debug("left_drive: {}; right_drive: {}".format(left_drive, right_drive))
        if left_drive >= 0:
            self.left_motor.forward(left_drive)
        else:
            self.left_motor.backward(-left_drive)
        if right_drive >= 0:
            self.right_motor.forward(right_drive)
        else:
            self.right_motor.backward(-right_drive)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()


class CamJamBot(Robot): 
    def __init__(self):
        super().__init__(left_a_pin=10, left_b_pin=9, right_a_pin=8, right_b_pin=7)


class AmyBot(Robot):
    def __init__(self):
        self.enable_left = LED(17)
        self.enable_right = LED(22)
        self.enable_left.off()
        self.enable_right.off()
        #super().__init__(left_a_pin=18, left_b_pin=27, right_a_pin=23, right_b_pin=24)
        super().__init__(left_a_pin=24, left_b_pin=23, right_a_pin=27, right_b_pin=18)
        self.enable_left.on()
        self.enable_right.on()
