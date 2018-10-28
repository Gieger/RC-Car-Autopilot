# Farhzeug.py
# Author: Dennis Gieger

#Klasse zum Bereitstellen des Kamerabildes
import time
import numpy as np
import cv2


class BasisKamera:
    
    def ausfuehren_parallel(self):
        return self.frame


class PiCamera(BasisKamera):
    name = "RPi-Kamera"

    def __init__(self, resolution=(480, 640), framerate=20):
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        resolution = (resolution[1], resolution[0])
        # initialize the camera and stream
        self.camera = PiCamera()  # PiCamera gets resolution (height, width)
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="rgb",
                                                     use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.on = True

        print('PiCamera loaded.. .warming camera')
        time.sleep(2)

    """
    def run(self):
        f = next(self.stream)
        frame = f.array
        self.rawCapture.truncate(0)
        return frame
    """

    def aktualisieren(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            if not self.on:
                break

    def beenden(self):
        # indicate that the thread should be stopped
        self.on = False
        print('stoping PiCamera')
        time.sleep(.5)
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()


class USB_kamera(BasisKamera):
    name = "USB-Kamera"
	
	#Kamera initialisierung
    def __init__(self, aufloesung=(120, 160), fps=30):

        aufloesung = (aufloesung[1], aufloesung[0])

        self.kamera = cv2.VideoCapture(-1)
        self.kamera.set(cv2.CAP_PROP_FRAME_WIDTH, aufloesung[0])
        self.kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, aufloesung[1])
        self.kamera.set(cv2.CAP_PROP_FPS, fps)

        self.bild = self.kamera.read()
        self.programm_laeuft = True
        
        time.sleep(2)

	#Endlosschleife für das Abgreifen der Bilder von der Kamera
    def aktualisieren(self):
        while self.programm_laeuft:
            erfolg, self.bild = self.kamera.read()

	# Thread beenden
    def beenden(self):
        self.programm_laeuft = False
        print('Kamera beenden')
        self.kamera.cap.release()
        time.sleep(.5)