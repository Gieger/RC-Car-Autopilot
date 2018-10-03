import smbus2 as smbus


import Fabo_PCA9685
import time

class PCA9685():
    name = "PWM"

    def __init__(self, frequency=50):
            self.BUSNUM=1
            self.INITIAL_VALUE=300
            self.bus = smbus.SMBus(self.BUSNUM)
            self.pwm = Fabo_PCA9685.PCA9685(self.bus,self.INITIAL_VALUE)
            self.pwm.set_hz(frequency)
            self.speed = 0
            self.angle = 0
            self.pspeed = 0
            self.pangle = 0
            self.assist = 0
            self.record = False
            self.stop_all = False


    def run_threaded(self, controller, predict):
        if controller[0] != None:
            self.speed = controller[0] * 50
            self.angle = controller[1] * 100
            self.record = controller[2]
            self.stop_all = controller[3]
            self.save = controller[4]
            self.assist = controller[5]

        if predict != None:
            pangle = predict

            self.pangle = pangle * 100

    def update(self):
        while True:
            if self.assist == False:
                #print(self.speed, self.angle)
                self.pwm.set_channel_value(3, 330 - self.speed)
                self.pwm.set_channel_value(12, 310 + self.angle)
                self.pwm.set_channel_value(13, 310 + self.angle)

            if self.assist == True:
                if self.stop_all == True:
                    self.pwm.set_channel_value(3, 350)
                else:
                    self.pwm.set_channel_value(3, 330 - self.speed)
                self.pwm.set_channel_value(12, 310 + self.pangle)
                self.pwm.set_channel_value(13, 310 + self.pangle)
                #print(self.speed, self.pangle)


