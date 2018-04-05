import enum
import time
import picamera
import threading
import picamera.array
import numpy as np
import cv2
from time import sleep
import logging
from imagecapture import ImageCapture
from streamprocessor import StreamProcessor


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
        stream = picamera.array.PiRGBArray(self.camera)
        event = threading.Event()
        capStream = ImageCapture(self.camera, stream, event)
        for colour in Colours:
            if event.wait(1):
                self.process(stream.array, colour)
                # eroded = cv2.erode(range, )
                LOGGER.debug(colour)
                sleep(2)
                #self.camera.capture('foo.jpg')
                range_data = ranges[colour]
                LOGGER.debug(range_data)
        capStream.terminated = True

    def process(self, image, colour, debug=False):
        if debug:
            cv2.imshow('original', image)
            cv2.waitKey(0)

        # Blur the image
        image = cv2.medianBlur(image, 5)
        if debug:
            cv2.imshow('blur', image)
            cv2.waitKey(0)

        # Convert the image from 'BGR' to HSV colour space
        image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        if debug:
            cv2.imshow('cvtColour', image)
            cv2.waitKey(0)

        # We want to extract the 'Hue', or colour, from the image. The 'inRange'
        # method will extract the colour we are interested in (between 0 and 180)
        # In testing, the Hue value for red is between 95 and 125
        # Green is between 50 and 75
        # Blue is between 20 and 35
        # Yellow is... to be found!
        imrange = cv2.inRange(image, np.array(ranges[colour]["low"]), np.array(ranges[colour]["high"]))

        # I used the following code to find the approximate 'hue' of the ball in
        # front of the camera
        #        for crange in range(0,170,10):
        #            imrange = cv2.inRange(image, numpy.array((crange, 64, 64)), numpy.array((crange+10, 255, 255)))
        #            print(crange)
        #            cv2.imshow('range',imrange)
        #            cv2.waitKey(0)

        # View the filtered image found by 'imrange'
        if debug:
            cv2.imshow('imrange', imrange)
            cv2.waitKey(0)

        # Find the contours
        contourimage, contours, hierarchy = cv2.findContours(imrange, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if debug:
            cv2.imshow('contour', contourimage)
            cv2.waitKey(0)

        # Go through each contour
        foundArea = -1
        foundX = -1
        foundY = -1
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cx = x + (w / 2)
            cy = y + (h / 2)
            area = w * h
            if foundArea < area:
                foundArea = area
                foundX = cx
                foundY = cy
        if foundArea > 0:
            ball = [foundX, foundY, foundArea]
        else:
            ball = None
        print(ball)

