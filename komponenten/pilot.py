from keras.models import load_model
import os
import sys
import numpy as np
import cv2
import utils
import time

class Fahrer:
    name = "Autoilot"
    def __init__(self):
        self.values = []      
        self.programm_laeuft = True
        self.bild = None
        self.beschleuniging = 0
        self.lenkung = 0
        self.plenkung = 0
        self.pbeschleuniging = -0.2
        self.mode = "Benutzer"
        print('Steuerung lädt...')

        print("KI laden")
        self.model = load_model('daten/modelle/model.h5')
        self.model._make_predict_function()
        print("KI bereit")
        time.sleep(4)
        
    def ausfuehren_parallel(self, kamera=None,beschleunigung=0, lenkung=0, mode="Benutzer"):
        self.bild = kamera
        self.mode = mode
        self.beschleuniging = beschleunigung
        self.lenkung = lenkung
        
        if self.mode == "Assistent":
            return self.plenkung, self.beschleuniging
        elif self.mode == "Automatik":
            return self.plenkung, self.pbeschleuniging
        else:
            return self.lenkung, self.beschleuniging




    def aktualisieren(self):
        time.sleep(1)
        while self.programm_laeuft:
            
            time.sleep(0.2)
            if self.mode == "Assistent" or "Automatik":

                __image = utils.preprocess(self.bild)

                #__image = np.expand_dims(__image, axis=0)

                __image1 = __image.reshape((-1, 66, 200, 3))

                #cv2.imshow("Yuv", __image)
                #cv2.waitKey(0)

                __outputs = self.model.predict(__image1, batch_size=1)
                steer = __outputs[0]
                steer = steer[0]

                #steer = steer * 2

                #print(steer)

                if steer < -1:
                    steer = -1
                if steer > 1:
                    steer = 1



                self.plenkung = steer


            

    def shutdown(self):
        self.on = False
        print('stoping Auotpilot')
        time.sleep(.5)
