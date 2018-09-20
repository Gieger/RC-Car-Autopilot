import time
import threading

from pwm import PCA9685
from camera import USB_Camera as Camera
from gamepad import Controller

class Trexxas_Summit(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    speed = None


    def __init__(self):
        if Trexxas_Summit.thread is None:
            # start background frame thread
            Trexxas_Summit.thread = threading.Thread(target=self._thread)
            Trexxas_Summit.thread.start()

    @classmethod
    def _thread(cls):
        camera = Camera()
        controller = Controller()
        while True:
            cls.speed = controller.speed
            cls.frame = camera.get_frame()