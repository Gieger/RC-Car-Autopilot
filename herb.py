from car import Trexxas_Summit
import numpy as np
import time
import cv2

def loop(trexxas):
    while True:
        #a = trexxas.get_frame()   
        while trexxas.frame is None:
            time.sleep(0)

        b = trexxas.frame
        print(b)
        cv2.imshow('frame',b)    
        time.sleep(2)

loop(Trexxas_Summit())