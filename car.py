from pwm import PCA9685

class Trexxas_Summit(object):

    def __init__(self):
        # Servo-data
        self.servo_steering1 = PCA9685(3)
        self.servo_steering2 = PCA9685(12)
        self.servo_esc = PCA9685(13)

    def set_speed(self, val):
        self.servo_esc.run(val)

    def set_steering(self, val):
        self.servo_steering1.run(val)
        self.servo_steering2.run(val)