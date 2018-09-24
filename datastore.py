import os
import sys
import time
import json
from datetime import datetime
import random
import tarfile

import numpy as np
import pandas as pd
from PIL import Image
import cv2
import csv

class Datastore:
    name = "Datastore"
    def __init__(self):
        self.values = []      
        self.on = True
        self.count = 0
        self.frame = None
        self.speed = None
        self.angle = None
        self.record = None
        self.stop_all = None
        self.save = None
        time.sleep(5)

    def run_threaded(self, camera, controller):
        self.frame = camera
        self.speed = controller[0]
        self.angle = controller[1]
        self.record = controller[2]
        self.stop_all = controller[3]
        self.save = controller[4]

    def update(self):
        while True:
            t = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
        
            path = "Data/Images/frame_" + str(t) + ".jpg"
            #cv2.imwrite(os.path.join(path , 'waka.jpg'),img)

            cv2.imwrite(path, self.frame)
            print(self.speed)
            self.values.append([path, self.speed, self.angle])

            self.count = self.count + 1
            if self.count == 10:
                myFile = open('csvexample3.csv', 'w')

                with myFile:  
                    writer = csv.writer(myFile, delimiter=',', quoting=csv.QUOTE_ALL)
                    writer.writerows(self.values)
            

    def shutdown(self):
        self.on = False
        print('stoping PiCamera')
        time.sleep(.5)
        self.stream.close()