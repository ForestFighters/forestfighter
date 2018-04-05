import threading
import time


class ImageCapture(threading.Thread):
    def __init__(self, camera, stream, event):
        super(ImageCapture, self).__init__()
        self.camera = camera
        self.stream = stream
        self.event = event
        self.terminated = False
        self.start()

    def run(self):
        print('Start the stream using the video port')
        self.camera.capture_sequence(self.TriggerStream(), format='bgr', use_video_port=True)
        print('Processing terminated.')

    # Stream delegation loop
    def TriggerStream(self):
        global running
        while not self.terminated:
            if self.event.is_set():
                time.sleep(0.01)
            else:
                yield self.stream
                self.event.set()
        print(self.terminated)