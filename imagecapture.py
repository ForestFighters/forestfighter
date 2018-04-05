import threading
import time


class ImageCapture(threading.Thread):
    def __init__(self, camera, processor):
        super(ImageCapture, self).__init__()
        self.camera = camera
        self.processor = processor
        self.start()

    def run(self):
        print('Start the stream using the video port')
        self.camera.capture_sequence(self.TriggerStream(), format='bgr', use_video_port=True)
        print('Terminating camera processing...')
        self.processor.terminated = True
        self.processor.join()
        print('Processing terminated.')

    # Stream delegation loop
    def TriggerStream(self):
        global running
        while running:
            if self.processor.event.is_set():
                time.sleep(0.01)
            else:
                yield self.processor.stream
                self.processor.event.set()