import enum
from picamera import PiCamera
from time import sleep

class Colours(enum.Enum):
    RED = 0
    BLUE = 1
    YELLOW = 2
    GREEN = 3

low_hue =  [0, 150, 35, 75, 20]		# red was 150 green was 40
high_hue = [ 10, 230, 75, 107, 35 ]	# red was 179 green was 85

low_sat = [ 158, 128, 127, 127, 85 ]
high_sat = [ 255, 255, 255, 255, 255 ]

low_v = [158, 0, 127, 127, 150]
high_v = [255, 255, 255, 255, 255]

class Rainbow(object):
    order = []
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
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
        self.camera.start_preview()
        # Camera warm-up time
        sleep(2)
        self.camera.capture('foo.jpg')

