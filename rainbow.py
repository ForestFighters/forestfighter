import enum
import time
import picamera
import numpy as np
import cv2
from time import sleep
import logging


LOGGER = logging.getLogger(__name__)


class Colours(enum.Enum):
    RED = 0
    RED1 = 1
    BLUE = 2
    YELLOW = 3
    GREEN = 4


ranges = {Colours.RED: {"low": (0, 158, 158), "high": (10, 255, 255)},
          Colours.RED1: {"low": (150, 128, 0), "high": (230, 255, 255)},
          Colours.BLUE: {"low": (35,127, 127), "high": (75, 255, 255)},
          Colours.YELLOW: {"low": (75,127, 127), "high": (107, 255, 255)},
          Colours.GREEN: {"low": (20,85,150), "high": (35, 255, 255)}}

class Rainbow(object):
    order = []
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.brightness = 50
        self.camera.framerate = 24
        # warm up
        time.sleep(2)
        # Camera.set(CV_CAP_PROP_FORMAT, CV_8UC3);
        # Camera.set(CV_CAP_PROP_FRAME_WIDTH, 640); // 320
        # Camera.set(CV_CAP_PROP_FRAME_HEIGHT, 480); // 240
        # Camera.set(CV_CAP_PROP_BRIGHTNESS, 50);
        #
        # if (!Camera.open() ) {
        # fprintf(stderr, "Failed to init open camera\n");
        # }
        #
        # if (viewing){
        # namedWindow("Original", CV_WINDOW_AUTOSIZE);
        # }

    def rainbow(self):
        for colour in Colours:
            image = np.empty((640 * 480 * 3,), dtype=np.uint8)
            self.camera.capture(image, 'bgr')
            image = image.reshape((640, 480, 3))
            range = cv2.inRange(image, np.array(ranges[colour]["low"]), np.array(ranges[colour]["high"]))
            cv2.imshow('range', range)
            cv2.waitKey(0)
            # eroded = cv2.erode(range, )
            LOGGER.debug(colour)
            sleep(2)
            #self.camera.capture('foo.jpg')
            range_data = ranges[colour]
            LOGGER.debug(range_data)

