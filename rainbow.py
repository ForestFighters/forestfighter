import enum
from picamera import PiCamera
from time import sleep

class Colours(enum.Enum):
    RED = 0
    RED1 = 1
    BLUE = 2
    YELLOW = 3
    GREEN = 4

ranges = {Colours.RED: {"hue": (0, 10), "sat": (158,255), "variance": (158,255)},
          Colours.RED1: {"hue": (150, 230), "sat": (128,255), "variance": (0,255)},
          Colours.BLUE: {"hue": (35,75), "sat": (127,255), "variance": (127,255)},
          Colours.YELLOW: {"hue": (75,107), "sat": (127,255), "variance": (127,255)},
          Colours.GREEN: {"hue": (20,35), "sat": (85,255), "variance": (150,255)}}

class Rainbow(object):
    order = []
    def __init__(self):
        self.camera = PiCamera()
        self.camera.zoom = (0, 0, 0.5, 0.5)
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
            print(colour.name)
            sleep(2)
            self.camera.capture('foo.jpg')
            range_data = ranges[colour]
            print(range_data)

