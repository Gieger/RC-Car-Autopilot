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

class Datastore:
    name = "Datastore"
    def __init__(self):      
        self.frame = None
        self.on = True

        print('Datastore loaded')
        time.sleep(5)

    def run(self, camera):
        t = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
        cv2.imwrite(str(t) + ".jpg", camera)

    def shutdown(self):
        self.on = False
        print('stoping PiCamera')
        time.sleep(.5)
        self.stream.close()