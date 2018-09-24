import time
import pkg_resources
import smbus2 as smbus
import Fabo_PCA9685


class PCA9685:
    def __init__(self, channel, frequency):
            self.BUSNUM=1
            self.INITIAL_VALUE=300
            self.bus = smbus.SMBus(self.BUSNUM)
            self.pwm = Fabo_PCA9685.PCA9685(self.bus,self.INITIAL_VALUE)
            self.pwm.set_hz(frequency)
            self.channel = channel

        def set_pulse(self, pulse):
            self.pwm.set_channel_value(self.channel, pulse)

        def run(self, pulse):
            self.set_pulse(pulse)
