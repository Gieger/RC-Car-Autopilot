import os
import sys
import time
from datetime import datetime
import numpy as np
import pandas as pd
import cv2
import csv

class Datenspeicher:
    name = "Datenspeicher"

    def __init__(self):
        self.werte = []      
        self.programm_laeuft = True
        self.bild = None
        self.beschleunigung = 0
        self.lenkung = 0
        self.besch_x = 0
        self.besch_y = 0
        self.besch_z = 0
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0
        self.aufnahme = False
        self.modus = "Benutzer"
        self.speichern = False
        print('Datenspeicher lädt...')

    def ausfuehren_parallel(self, kamera, beschleunigung=0, lenkung=0, aufnahme=0, speichern=0, besch_x = 0, besch_y = 0, besch_z = 0, gyro_x = 0, gyro_y = 0, gyro_z = 0):
        self.bild = kamera
        self.beschleunigung = beschleunigung
        self.lenkung = lenkung
        self.besch_x = besch_x
        self.besch_y = besch_y
        self.besch_z = besch_z
        self.gyro_x = gyro_x
        self.gyro_y = gyro_y
        self.gyro_z = gyro_z
        self.aufnahme = aufnahme
        self.speichern = speichern
        #print(aufnahme)

    def aktualisieren(self):
        while self.programm_laeuft:
            time.sleep(0.2)
            if self.aufnahme == True:
                #if self.beschleunigung != 0:
                zeitstempel = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]

                pfad = "daten/bilder/bild_" + str(zeitstempel) + ".jpg"
                cv2.imwrite(pfad, self.bild)
                #cv2.imwrite(os.path.join(path , 'waka.jpg'),img)

                self.werte.append([pfad, self.beschleunigung, self.lenkung, self.besch_x, self.besch_y, self.besch_z, self.gyro_x, self.gyro_y, self.gyro_z])

                #print(self.beschleunigung, self.aufnahme, self.besch_x, self.besch_y, self.besch_z, self.gyro_x, self.gyro_y, self.gyro_z)

            if self.speichern == True:
                zeitstempel = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
            
                pfad = "daten/logs/Log_" + str(zeitstempel) + ".csv"
                datei = open(pfad, 'w')

                time.sleep(5)

                with datei:  
                    writer = csv.writer(datei, delimiter=',', quoting=csv.QUOTE_ALL)
                    writer.writerows(self.werte)

    def beenden(self):
        self.programm_laeuft = False
        print('Datenspeicher beenden')
        time.sleep(.5)
