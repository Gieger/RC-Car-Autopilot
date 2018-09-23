import os
import time
import numpy as np
from PIL import Image
import glob
import cv2

class USB_Camera():
    name = "USB-Camera"
    def __init__(self, resolution=(120, 160), fps=30):    
        resolution = (resolution[1], resolution[0])

        self.camera = cv2.VideoCapture(0) 
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
        self.camera.set(cv2.CAP_PROP_FPS, fps)

        self.frame = self.camera.read()
        self.on = True

        print('USB-Camera loaded.. .warming camera')
        time.sleep(2)

    def run_threaded(self):
        return self.frame

    def update(self):
        self.running=True
        while self.running:
            ret, self.frame = self.camera.read()

            #if not self.on:
            #    break

    def shutdown(self):
        self.on = False
        print('stoping PiCamera')
        time.sleep(.5)
        self.stream.close()
        self.camera.cap.release()
        self.camera.close()