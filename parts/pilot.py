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
        self.record = False
        self.stop_all = None
        self.save = False
        self.psteering = None
        self.pthrottel = None
        print('Autopilot loading')

        print("Load Model")
        self.model = load_model('/home/nvidia/RC-Car-Autopilot/Data/Model/model-001.h5')
        self.model._make_predict_function()
        print("Model bereit")
 
        
    def run_threaded(self, camera):
        self.frame = camera
        return self.psteering, self.pthrottel


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
                steer = __outputs[0][0]
                throt = __outputs[0][1]

                #print(steer, throt)

                if steer < -1:
                    steer = -1
                if steer > 1:
                    steer = 1

                if throt < -1:
                    throt = -1
                if throt > 1:
                    throt = 1

                self.pthrottel = throt
                self.psteering = steer


            

    def shutdown(self):
        self.on = False
        print('stoping Auotpilot')
        time.sleep(.5)
