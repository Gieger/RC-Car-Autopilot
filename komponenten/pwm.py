# pwm.py
# Author: Dennis Gieger

# Bibliotheken import
from __future__ import division

# Basis Klasse
class BasisPWM:
    programm_laeuft = True
    beschleuniging = 0
    lenkung = 0

	# Methode für die ein und ausgabe 
    def ausfuehren_parallel(self, beschleuniging, lenkung):
        self.beschleuniging = beschleuniging
        self.lenkung = lenkung



	# Thread beenden
    def beenden(self):
        self.programm_laeuft = False
        print('PWM beenden')
        time.sleep(.5)

		
# Klasse zur Regelung des Motors und Lenkservos für JetsonTX2
class Fabo_PCA9685(BasisPWM):
    name = "PWM"

	# PWM initialisierung
    def __init__(self, frequenz=50):
            import smbus2 as smbus
            import Fabo_PCA9685

            self.BUSNUM=1
            self.INITIAL_VALUE=300
            self.bus = smbus.SMBus(self.BUSNUM)
            self.pwm = Fabo_PCA9685.PCA9685(self.bus,self.INITIAL_VALUE)
            self.pwm.set_hz(frequenz)
            print('PWM lädt...')

	# Endlosschleife für die Regelung
    def aktualisieren(self):
        while self.programm_laeuft:
            self.pwm.set_channel_value(3, 330 - self.beschleuniging)
            self.pwm.set_channel_value(12, 310 + self.lenkung)
            self.pwm.set_channel_value(13, 310 + self.lenkung)

# Klasse zur Regelung des Motors und Lenkservos für Raspberry Pi
class PCA9685(BasisPWM):
    name = "PWM"
    
	# PWM initialisierung
    def __init__(self, frequenz=60):
        import Adafruit_PCA9685

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)

	# Endlosschleife für die Regelung
    def aktualisieren(self):
        while self.programm_laeuft:
            #print(self.beschleuniging,self.lenkung)
            self.pwm.set_pwm(12,0, 400 + int(self.beschleuniging*150))
            self.pwm.set_pwm(3,0, 400 + int(self.lenkung*120))
