import time
import pkg_resources
import smbus

class PCA9685:

    def __init__(self, channel):
        import Fabo_PCA9685
        self.BUSNUM=1
        self.frequency=50
        self.INITIAL_VALUE=300
        self.bus = smbus.SMBus(self.BUSNUM)
        self.pwm = Fabo_PCA9685.PCA9685(self.bus,self.INITIAL_VALUE)
        self.pwm.set_hz(self.frequency)
        self.channel = channel

    def set_pulse(self, pulse):
        self.pwm.set_channel_value(self.channel, pulse)

    def run(self, pulse):
        self.set_pulse(pulse)