import time
import threading



class Datastore(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    speed = None
    angle = None


    def __init__(self):
        if Datastore.thread is None:
            # start background frame thread
            Datastore.thread = threading.Thread(target=self._thread)
            Datastore.thread.start()

    @classmethod
    def _thread(cls):
        camera = Camera()
        controller = Controller()
        while True:
            cls.speed = controller.speed
            cls.throttle = controller.angle
            cls.frame = camera.get_frame()