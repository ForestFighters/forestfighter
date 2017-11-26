#!/usr/bin/env python
# coding: Latin-1

import time
import sys
from argparse import ArgumentParser
from robot import AmyBot, CamJamBot
import logging


def main(amybot=True, camjambot=False):
    if amybot:
        bot = AmyBot()
    else:
        bot = CamJamBot()

    bot.left_motor.forward()
    bot.right_motor.forward()

    time.sleep (5)
    sys.exit (0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = ArgumentParser()
    # either amybot or camjambot can be passed in, but not both.
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--amybot", help="Use the kit amy has (whatever Jim provided)")
    group.add_argument("--camjambot", help="Use the camjam edubot kit")
    args = parser.parse_args()

    main(args.amybot, args.camjambot)
