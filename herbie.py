from __future__ import division
from evdev import InputDevice, categorize, ecodes, KeyEvent
from datetime import datetime 
from keras.models import load_model

import argparse
import Adafruit_PCA9685
import cv2
import csv
import os
import glob
import time
import random
import threading
import numpy as np

import utils


class Gamepad(threading.Thread):
    end = False
    autopilot = False
    assist = False
    flag = False
    steering = 0
    throttle = 0
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.gamepad = InputDevice('/dev/input/event1')
        
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)
        self.pwm.set_pwm(3, 0, 370)
        self.pwm.set_pwm(12, 0, 300) 
        
    def run(self):        
        print("Pad ON")
        try:
            for event in self.gamepad.read_loop():
                if Gamepad.autopilot == False:
                    if event.type == ecodes.EV_ABS:
                        absevent = categorize(event)
                        
                        if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                            if absevent.event.value == 255:
                                self.pwm.set_pwm(12, 0, 300)
                                Gamepad.throttle = float(0)
                            
                            elif absevent.event.value >= 1:
                                pass
                                #self.pwm.set_pwm(12, 0, 310)
                        
                            elif absevent.event.value <= -1:
                                __throttle = float((absevent.event.value) / 32768)
                                #__throttle_new = int(__throttle * 20)
                                self.pwm.set_pwm(12, 0, 330)
                                Gamepad.throttle = __throttle
                        if Gamepad.assist == False:
                            if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RX':
                                if absevent.event.value == 0:                   
                                    self.pwm.set_pwm(3, 0, 370)
                                    Gamepad.steering = float(0)
                                                        
                                elif absevent.event.value <= -1:        
                                    __steering = float((absevent.event.value) / 32768)
                                    __steering_new = int(__steering * 120)

                                    self.pwm.set_pwm(3, 0, 370 - __steering_new)
                                    Gamepad.steering = __steering

                                elif absevent.event.value >= 1:
                                    __steering = float((absevent.event.value) / 32767)
                                    __steering_new = int(__steering * 120)

                                    self.pwm.set_pwm(3, 0, 370 - __steering_new)
                                    Gamepad.steering = __steering



                        

                if event.type == ecodes.EV_KEY:
                    keyevent = categorize(event)
                    if keyevent.keystate == KeyEvent.key_down:
                        if keyevent.keycode[0] == 'BTN_B':
                            if Gamepad.assist == True:
                                Gamepad.autopilot = True
                                print("Autopilot ON")
                        elif keyevent.keycode[0] == 'BTN_NORTH':
                            print("Assist OFF")
                            Gamepad.assist = False
                            Gamepad.autopilot = False
                        elif keyevent.keycode[0] == 'BTN_WEST':
                            print("Autopilot OFF")
                            Gamepad.autopilot = False
                        elif keyevent.keycode[0] == 'BTN_A':
                            if Gamepad.autopilot == False & Gamepad.assist == False:
                                print("Assist ON")
                                Gamepad.assist = True
                        elif keyevent.keycode == 'BTN_TR':
                            print("Record ON")
                            Gamepad.flag = True
                        elif keyevent.keycode == 'BTN_TL':                           
                            Gamepad.flag = False
                            print("Record OFF")
                        elif keyevent.keycode == 'BTN_START':
                            Gamepad.end = True                           
                        #elif keyevent.keycode == 'BTN_THUMBR':
                        #    self.pwm.set_pwm(12, 0, 310)

                if Gamepad.end == True:
                    print("Program Ende")
                    break
                    
        except IOError:
            print("Pad OFF")
            self.pwm.set_pwm(12, 0, 300)
            #self.pwm.set_pwm(0, 0, 330)
            self.pwm.set_pwm(3, 0, 370)


class Camera(threading.Thread):
    image = None

    def __init__(self):
        threading.Thread.__init__(self)
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 160);
        time.sleep(2)
        
    def run(self):
        print("Cam ON")
        while True:
            return_value, Camera.image = self.camera.read()


class Drive(threading.Thread):
    steer = float(0)
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)
        self.pwm.set_pwm(3, 0, 370)
        self.pwm.set_pwm(12, 0, 300)
                
    def run(self):          
        try:
            print("Load Model")
            self.model = load_model('Data/Model/model.h5')
            print("Model bereit")
            

            while True:
                if Gamepad.assist == True:
                    __image = Camera.image
                    __image = utils.preprocess(__image)
                    __image = np.asarray(__image, dtype=np.float32)
                    __image = np.array([__image])           

                    __steering_angle = float(self.model.predict(__image, batch_size=1))

                    if __steering_angle < -1:
                        __steering_angle = -1
                    if __steering_angle > 1:
                        __steering_angle = 1
                    
                    Drive.steer = __steering_angle
                    __steer = int(__steering_angle * 120)
                    print ("Lenken ------------------")
                    print(Drive.steer)
                    self.pwm.set_pwm(3, 0, 370 - __steer)
                    #self.pwm.set_pwm(3, 0, 330 + __steer)
                
                
        except IOError:
            print("-----Model Datei fehlt !!!-----") 
        

class Record(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.t = datetime.utcnow().strftime('%Y_%m_%d_%H_%M')[:-3]   
        self.out = csv.writer(open("Data/Log/" + str(self.t) + ".csv", "w"), delimiter=',')

    def run(self):            
        while Gamepad.end == False:
            if Gamepad.flag == True:

                time.sleep(0.1)
                self.t = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]

                lockMe.acquire()
                __image = Camera.image
                __throttle = Gamepad.throttle
                __steering = Gamepad.steering
                lockMe.release()

                cv2.imwrite("Data/Image/center_"+ str(self.t) + ".jpg", __image)
                cv2.imwrite("Data/Image/left_"+ str(self.t) + ".jpg", __image)
                cv2.imwrite("Data/Image/right_"+ str(self.t) + ".jpg", __image)          
                
                self.r = "/home/ocp/Schreibtisch/Herbie/Data/Image/center_"+ str(self.t) + ".jpg", "/home/ocp/Schreibtisch/Herbie/Data/Image/left_"+ str(self.t) + ".jpg", "/home/ocp/Schreibtisch/Herbie/Data/Image/right_"+ str(self.t) + ".jpg", __steering, __throttle ,"0","0"

                self.out.writerow(self.r)
                print("--------------------")
                print(__steering)
                print(__throttle)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Herbie Autonomous RC-Car')
    parser.add_argument('-m', help='Modelfile', dest='model', type=str,  default='model.h5')
    parser.add_argument('-a', help='Autopilot', dest='auto' , type=bool, default=False)
    
    args = parser.parse_args()

    lockMe = threading.Lock()
    pad = Gamepad()
    cam = Camera()
    rec = Record()
    car = Drive()

    pad.start()
    cam.start()
    rec.start()
    car.start()
