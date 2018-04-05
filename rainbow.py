import enum
from picamera import PiCamera
from time import sleep

class Colours(enum.Enum):
    RED = 0
    BLUE = 1
    YELLOW = 2
    GREEN = 3


class Rainbow(object):
    order = []
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)

    def rainbow(self):
        self.camera.start_preview()
        # Camera warm-up time
        sleep(2)
        self.camera.capture('foo.jpg')