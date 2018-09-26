#import smbus2 as smbus


#import Fabo_PCA9685
import time

class PCA9685():
    name = "PWM"

    def __init__(self, frequency=50):
            self.BUSNUM=1
            self.INITIAL_VALUE=300
 #           self.bus = smbus.SMBus(self.BUSNUM)
#            self.pwm = Fabo_PCA9685.PCA9685(self.bus,self.INITIAL_VALUE)
  #          self.pwm.set_hz(frequency)
            self.speed = 0
            self.angle = 0


    def run_threaded(self, controller):
        if controller[0] != None:
            speed = controller[0]
            angle = controller[1]
            self.speed = speed * 50
            self.angle = angle * 100

    def update(self):
        time.sleep(8)
        mode = "auto"
        while True:
            if mode == 'User':
                print(self.speed, self.angle)
                self.pwm.set_channel_value(3, 330 - self.speed)
                self.pwm.set_channel_value(12, 310 + self.angle)
                self.pwm.set_channel_value(13, 310 + self.angle)

            elif mode == 'auto':
                print(self.speed, self.angle)