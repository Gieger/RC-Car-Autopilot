import time
from mpu6050 import mpu6050

class Mpu6050:
    name = "Gyroskope"

    def __init__(self, addr=0x68, poll_delay=0.0166):

        self.sensor = mpu6050(addr)
        self.accel = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.gyro = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.temp = 0.
        self.poll_delay = poll_delay
        self.on = True

    def aktualisieren(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)

    def poll(self):
        self.accel, self.gyro, self.temp = self.sensor.get_all_data()

    def ausfuehren_parallel(self):
        return self.accel['x'], self.accel['y'], self.accel['z'], self.gyro['x'], self.gyro['y'], self.gyro['z']

    def ausfuehren(self):
        self.poll()
        return self.accel['x'], self.accel['y'], self.accel['z'], self.gyro['x'], self.gyro['y'], self.gyro['z'], self.temp

    def beenden(self):
        self.on = False

