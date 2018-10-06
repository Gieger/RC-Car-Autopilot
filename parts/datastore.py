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
        self.frame = None
        self.speed = 0
        self.angle = 0
        self.record = False
        self.mode = "User"
        self.save = False
        print('Datastore loading')

        time.sleep(5)

    def run_threaded(self, camera, speed, angle, record, save):
        self.frame = camera
        self.speed = speed
        self.angle = angle
        self.record = record
        self.save = save

    def update(self):
        while self.on:
            if self.record == True:
                if self.speed != 0:
                    t = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
                    time.sleep(.1)
                    path = "data/images/frame_" + str(t) + ".jpg"
                    #cv2.imwrite(os.path.join(path , 'waka.jpg'),img)

                    cv2.imwrite(path, self.frame)
                    self.values.append([path, self.speed, self.angle])
                    print(self.speed, self.angle)

            if self.save == True:
                t = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
            
                path = "data/logs/Log_" + str(t) + ".csv"
                myFile = open(path, 'w')

                with myFile:  
                    writer = csv.writer(myFile, delimiter=',', quoting=csv.QUOTE_ALL)
                    writer.writerows(self.values)

                self.values = []
                time.sleep(5)
            

    def shutdown(self):
        self.on = False
        print('stoping Datastore')
        time.sleep(.5)
