from __future__ import division
import time

class _Fabo_PCA9685():
    name = "PWM"

    def __init__(self, frequency=50):
            import smbus2 as smbus
            import Fabo_PCA9685
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



    def run_threaded(self, values):
        if controller[0] != None:
            self.speed = speed
            self.angle = angle
            self.mode = mode

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


class PCA9685():
    name = "PWM"
    def __init__(self, frequency=60):

        import Adafruit_PCA9685

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)
        self.on = True
        self.speed = 0
        self.angle = 0


    def run_threaded(self, speed, angle):       
            self.speed = speed
            self.angle = angle

    def update(self):
        while self.on:
            self.pwm.set_pwm(12,0, 300 - int(self.speed*50))
            self.pwm.set_pwm(3,0, 370 + int(self.angle*140))
