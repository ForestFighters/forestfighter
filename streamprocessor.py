import threading
import picamera
import cv2

class StreamProcessor(threading.Thread):
    def __init__(self, camera):
        super(StreamProcessor, self).__init__()
        self.stream = picamera.array.PiRGBArray(camera)
        self.event = threading.Event()
        self.terminated = False
        self.start()
        self.begin = 0

    def run(self):
        # This method runs in a separate thread
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    # Read the image and do some processing on it
                    self.stream.seek(0)
                    self.ProcessImage(self.stream.array, colour)
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()

    # Image processing function
    def ProcessImage(self, image, colour):
        # View the original image seen by the camera.
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
        if colour == "red":
            imrange = cv2.inRange(image, numpy.array((95, 127, 64)), numpy.array((125, 255, 255)))
        elif colour == "green":
            imrange = cv2.inRange(image, numpy.array((50, 127, 64)), numpy.array((75, 255, 255)))
        elif colour == 'blue':
            imrange = cv2.inRange(image, numpy.array((20, 64, 64)), numpy.array((35, 255, 255)))

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
        # Set drives or report ball status
        self.SetSpeedFromBall(ball)

    # Set the motor speed from the ball position
    def SetSpeedFromBall(self, ball):
        global TB
        driveLeft = 0.0
        driveRight = 0.0
        if ball:
            x = ball[0]
            area = ball[2]
            if area < autoMinArea:
                print('Too small / far')
            elif area > autoMaxArea:
                print('Close enough')
            else:
                if area < autoFullSpeedArea:
                    speed = 1.0
                else:
                    speed = 1.0 / (area / autoFullSpeedArea)
                speed *= autoMaxPower - autoMinPower
                speed += autoMinPower
                direction = (x - imageCentreX) / imageCentreX
                if direction < 0.0:
                    # Turn right
                    print('Turn Right')
                    driveLeft = speed
                    driveRight = speed * (1.0 + direction)
                else:
                    # Turn left
                    print('Turn Left')
                    driveLeft = speed * (1.0 - direction)
                    driveRight = speed
                print('%.2f, %.2f' % (driveLeft, driveRight))
        else:
            print('No ball')