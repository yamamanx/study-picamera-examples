from imutils.video.pivideostream import PiVideoStream
import time
from datetime import datetime
import numpy as np
import cv2
from pyzbar import pyzbar
from picamera.array import PiRGBArray
from picamera import PiCamera


class QRDetector(object):
    def __init__(self, flip = False):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        time.sleep(0.1)
        #self.vs = PiVideoStream(resolution=(800, 608)).start()
        #self.flip = flip
        #time.sleep(2.0)

    def gen(self):
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        #frame = self.flip_if_needed(self.vs.read())
        #frame = self.process_image(frame)
        #ret, jpeg = cv2.imencode('.jpg', frame)
        #return jpeg.tobytes()

        self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
        frame = self.rawCapture.array
        decoded_objs = self.decode(frame)
        frame = self.display(frame, decoded_objs)
        ret, jpeg = cv2.imencode('.jpg', frame)
        self.rawCapture.truncate(0)

        return jpeg.tobytes()
        
    def process_image(self, frame):
        pass

    def decode(self, frame):
        decoded_objs = pyzbar.decode(frame, scan_locations=True)
        for obj in decoded_objs:
            print(datetime.now().strftime('%H:%M:%S.%f'))
            print('Type: ', obj.type)
            print('Data: ', obj.data)

        return decoded_objs

    def display(self, frame, decoded_objs):
        for decoded_obj in decoded_objs:
            left, top, width, height = decoded_obj.rect
            frame = cv2.rectangle(frame,
                                  (left, top),
                                  (left + width, height + top),
                                  (0, 0, 255), 2)
        return frame

    def draw(self, frame, decoded_objs):
        pass
    

