from car import Trexxas_Summit
import numpy as np
import time
from cv2 import cv2
import csv
from datetime import datetime

def loop(trexxas):
    speed = 0.0
    angle = 0.0
    while True:
        timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M')[:-3] 
        out = csv.writer(open("Data/Log/" + str(timestamp) + ".csv", "w"), delimiter=',')
        #a = trexxas.get_frame()   
        while trexxas.frame is None:
            time.sleep(0)


        if trexxas.flag_rec == True:
            time.sleep(1)
            frame = trexxas.frame
            speed = trexxas.speed
            angle = trexxas.angle
            print(speed,angle)
            timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]


            cv2.imwrite("Data/Image/center_"+ str(timestamp) + ".jpg", frame)          
            
            row = "/home/ocp/Schreibtisch/Herbie/Data/Image/center_", angle, speed

            out.writerow(row)
  

loop(Trexxas_Summit())