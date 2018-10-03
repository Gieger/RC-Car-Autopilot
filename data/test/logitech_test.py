from __future__ import division
from evdev import InputDevice, categorize, ecodes, KeyEvent
import time
import cv2
import numpy as np
import threading

class BasePad:
    def __init__(self):      
        self.left_dpad_y = None
        self.right_dpad_x = None
        self.a_button = None
        self.b_button = None
        self.x_button = None
        self.y_button = None
        self.start_button = None
        self.l1_button = None
        self.r1_button = None
        self.r3_button = None


class LogitechF710(BasePad):
    def __init__(self):
        self.logitech710 = InputDevice('/dev/input/event11')


class Gamepad(threading.Thread):  
    def __init__(self):
        threading.Thread.__init__(self)
        self.gamepad = LogitechF710()

    def run(self):        
        print("Pad ON")

        for event in self.gamepad.logitech710.read_loop():
            if event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_RX':
                    self.gamepad.right_dpad_x = absevent.event.value

                if ecodes.bytype[absevent.event.type][absevent.event.code] == 'ABS_Y':
                    self.left_dpad = absevent.event.value
                            
            if event.type == ecodes.EV_KEY:
                keyevent = categorize(event)
                if keyevent.keystate == KeyEvent.key_down:
                    if keyevent.keycode == 'BTN_B':
                        self.b_button = True

                    elif keyevent.keycode == 'BTN_NORTH':
                        self.y_button = True

                    elif keyevent.keycode == 'BTN_WEST':
                        self.x_button = True

                    elif keyevent.keycode[0] == 'BTN_A':
                        self.a_button = True

                    elif keyevent.keycode == 'BTN_TR':
                        self.r1_button = True
                        print("True")

                    elif keyevent.keycode == 'BTN_TL':
                        self.l1_button = True

                    elif keyevent.keycode == 'BTN_START':
                        self.start_button = True

                    elif keyevent.keycode == 'BTN_THUMBR':
                        self.r3_button = True

                if keyevent.keystate == KeyEvent.key_up:
                    if keyevent.keycode == 'BTN_B':
                        self.b_button = False
                        print("False")

                    elif keyevent.keycode == 'BTN_NORTH':
                        self.y_button = False

                    elif keyevent.keycode == 'BTN_WEST':
                        self.x_button = False

                    elif keyevent.keycode[0] == 'BTN_A':
                        self.a_button = False

                    elif keyevent.keycode == 'BTN_TR':
                        self.r1_button = False

                    elif keyevent.keycode == 'BTN_TL':
                        self.l1_button = False

                    elif keyevent.keycode == 'BTN_START':
                        self.start_button = False

                    elif keyevent.keycode == 'BTN_THUMBR':
                        self.r3_button = False