# Import time
from __future__ import division
import time

# Import PCA9685 Modul
import Adafruit_PCA9685

# Initialisieren des Standart PCA9685
# Alternative "pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)"
pwm = Adafruit_PCA9685.PCA9685()

# Konfiguration der Pulsweitenlänge
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Hilfsfunktion für Servo Puls
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    
    pulse_length //= 60       
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Frequenz auf 60Hz (Servo Standartwert)
pwm.set_pwm_freq(60)

# Ausgabe Servowerte
y = input("Channel ")

#Endlosschleife zur Eingabe von Sevowerten in Grad
while True:
    x = input("PWM ")
    print (x)
    pwm.set_pwm(int(y), 0, int(x))


