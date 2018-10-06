from keras.models import load_model
import os
import sys
import numpy as np
import cv2
import utils
import time

class Pilot:
    name = "Autoilot"
    def __init__(self):
        self.values = []      
        self.on = True
        self.count = 0
        self.frame = None
        self.speed = None
        self.angle = None
        self.mode = "User"
        print('Steuerung lädt...')

        print("KI laden")
        self.model = load_model('/home/nvidia/Desktop/homegeht/RC-Car-Autopilot/data/models/model-024.h5')
        self.model._make_predict_function()
        print("KI bereit")
 
        
    def run_threaded(self, camera):
        self.frame = camera
        return self.angle


    def update(self):
        time.sleep(5)
        while self.on:
            if self.on == True:

                __image = utils.preprocess(self.frame)

                #__image = np.expand_dims(__image, axis=0)

                __image1 = __image.reshape((-1, 66, 200, 3))

                #cv2.imshow("Yuv", __image)
                #cv2.waitKey(0)

                __outputs = self.model.predict(__image1, batch_size=1)
                steer = __outputs[0]
                steer = steer[0]

                steer = steer * 2

                #print(steer)

                if steer < -1:
                    steer = -1
                if steer > 1:
                    steer = 1



                self.psteering = steer


            

    def shutdown(self):
        self.on = False
        print('stoping Auotpilot')
        time.sleep(.5)
