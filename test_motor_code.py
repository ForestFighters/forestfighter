#!/usr/bin/env python
# coding: Latin-1

import time
import sys
from argparse import ArgumentParser
from robot import AmyBot, CamJamBot, FourTronix
import logging


def main(amybot=True, camjambot=False, fourtronix=False):
    if amybot:
        bot = AmyBot()
    elif camjambot:
        bot = CamJamBot()
    elif fourtronix:
        bot = FourTronix()
    else:
        print("Unknown Robot Type")
        sys.exit(0)        

    bot.left_motor.forward()
    bot.right_motor.forward()
    time.sleep (5)
    
    bot.left_motor.reverse()
    bot.right_motor.reverse()
    time.sleep (5)
    
    bot.left_motor.stop()
    bot.right_motor.stop()
    time.sleep (1)
    sys.exit (0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser()
    # either fortronix, amybot or camjambot can be passed in, but only one.
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--amybot", help="Use the kit amy has (whatever Jim provided)", action="store_true")
    group.add_argument("--camjambot", help="Use the camjam edubot kit", action="store_true")
    group.add_argument("--fourtronix", help="Use the 4tronix controller", action="store_true")
    args = parser.parse_args()

    main(args.amybot, args.camjambot, args.fourtronix)
