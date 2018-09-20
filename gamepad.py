from evdev import InputDevice, categorize, ecodes
import threading



class Controller(object):
    thread = None  # background thread that reads frames from camera
    speed = None  # current frame is stored here by background thread
    throttle = None

    def __init__(self):
        if Controller.thread is None:
            # start background frame thread
            Controller.thread = threading.Thread(target=self._thread)
            Controller.thread.start()

    @classmethod
    def _thread(cls):

        gamepad = InputDevice('/dev/input/event3')

        print(gamepad)

        aBtn = 305
        bBtn = 306
        xBtn = 304
        yBtn = 307
        lBtn = 308
        rBtn = 309
        selBtn = 312
        staBtn = 313

        
        for event in gamepad.read_loop():
            if event.type == ecodes.EV_KEY:
                #print(event)
                if event.value == 1:
                    if event.code == xBtn:
                        print("X")
                    elif event.code == bBtn:
                        print("B")
                    elif event.code == aBtn:
                        print("A")
                    elif event.code == yBtn:
                        print("Y")
                    elif event.code == lBtn:
                        print("LEFT")
                    elif event.code == rBtn:
                        print("RIGHT")
                    elif event.code == selBtn:
                        print("Select")
                    elif event.code == staBtn:
                        print("Start")
                elif event.value == 0:
                    print("Relache | Release")

            elif event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                #print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value

                if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
                    if absevent.event.value <= 120:                  
                        cls.speed = float(absevent.event.value)
                    elif absevent.event.value >= 134:
                        cls.speed = float(absevent.event.value)
                    elif absevent.event.value >= 121 or absevent.event.value <= 133:
                        cls.speed = float(0)

                elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Z":
                    if absevent.event.value <= 121:
                        print("Left")
                    elif absevent.event.value >= 133:
                        print("Right")
                    elif absevent.event.value >= 122 or absevent.event.value <= 132:
                        print("Center")
