# steuerung.py
# Author: Dennis Gieger

# Bibliotheken import
from inputs import get_gamepad
import time

# Basis Klasse
class BasisSteuerung:
    ereignisse = None
    beschleunigung = 0
    lenkung = 0
    aufnahme = False
    modus = "Benutzer"
    speichern = False
    programm_ende = False
    programm_laeuft = True

	# Methode für die Ein- und Ausgabe  
    def ausfuehren_parallel(self):
        return self.beschleunigung, self.lenkung, self.aufnahme, self.modus, self.speichern, self.programm_ende

	# Thread beenden
    def beenden(self):
        self.programm_laeuft = False
        print('Steuerung beenden')
        time.sleep(.5)

# Klasse zur Steuerung des Programmes und des Farhzeuges für Windows
class Logitech_F710(BasisSteuerung):
    name = "Gamepad"
    
	#Gamepad initialisierung
    def __init__(self):
        print('Controller loading')

	# Endlosschleife für das Abgreifen der Werte des Gamepads
    def aktualisieren(self):
        while self.programm_laeuft:
            self.ereignisse = get_gamepad()

			# Schleife zum Abfragen des Gamepad Status der Buttons
            for ereignis in self.ereignisse:
                if ereignis.ev_type == 'Absolute':  
                    if ereignis.code == 'ABS_Y':
                        wert = ereignis.state
                        if wert == 255:
                            self.beschleunigung = float(0)
                        if wert > 255:
                            self.beschleunigung = float(wert / 32767)
                        if wert < -255:
                            self.beschleunigung = float(wert / 32768)
                        #print(self.beschleunigung)

                    elif ereignis.code == 'ABS_RX':
                        if ereignis.state == 0:
                            self.lenkung = float(0)
                        if ereignis.state > 0:
                            self.lenkung = float(ereignis.state / 32767)
                        if ereignis.state < 0:
                            self.lenkung = float(ereignis.state / 32768)

				# Schleife zur steuerung der Programmlogik
                if ereignis.ev_type == 'Key':  
                    if ereignis.code == 'BTN_START':
                        if ereignis.state == 1:
                            self.speichern = True
                            print('Gespeichert')

                        if ereignis.state == 0:
                            self.speichern = False

                    if ereignis.code == 'BTN_SELECT':
                        if ereignis.state == 1:
                            self.programm_ende = True
                            print('Programm beendet')

                    if ereignis.code == 'BTN_TR':
                        if ereignis.state == 1:
                            self.aufnahme = True
                            print('Aufnahme EIN')

                    if ereignis.code == 'BTN_TL':
                        if ereignis.state == 1:
                            self.aufnahme = False
                            print('Aufnahme AUS')

                    if ereignis.code == 'BTN_SOUTH':
                        if ereignis.state == 1:
                            self.modus = "Manuell"
                            print('Manueller-Modus')

                    if ereignis.code == 'BTN_NORTH':
                        if ereignis.state == 1:
                            self.modus = "Assistent"
                            print('Lenkasisstent-Modus')  

                    if ereignis.code == 'BTN_WEST':
                        if ereignis.state == 1:
                            self.modus = "Automatik"
                            print('Autonomer-Modus') 

							
# Klasse zur Steuerung des Programmes und des Farhzeuges für Linux
class Xbox_F710(BasisSteuerung):
    name = "Gamepad"

	#Gamepad initialisierung
    def __init__(self):
        print('Controller loading')

	# Endlosschleife für das Abgreifen der Werte des Gamepads
    def aktualisieren(self):
        while self.programm_laeuft:
            self.ereignisse = get_gamepad()

			# Schleife zum Abfragen des Gamepad Status der Buttons
            for ereignis in self.ereignisse:
                if ereignis.ev_type == 'Absolute':
                    if ereignis.code == 'ABS_Y':
                        if ereignis.state == 127:
                            self.beschleunigung = float(0)
                        if ereignis.state > 127:
                            self.beschleunigung = float((ereignis.state - 127) / 128)
                        if ereignis.state < 127:
                            self.beschleunigung = float((ereignis.state - 127) / 127)

                    elif ereignis.code == 'ABS_Z':
                        if ereignis.state == 128:
                            self.lenkung = float(0)
                        if ereignis.state > 128:
                            self.lenkung = float((ereignis.state - 128) / 127)
                        if ereignis.state < 128:
                            self.lenkung = float((ereignis.state - 128) / 128)

				# Schleife zur steuerung der Programmlogik
                if ereignis.ev_type == 'Key':  
                    if ereignis.code == 'BTN_TR2':
                        if ereignis.state == 1:
                            self.speichern = True
                            print('Gespeichert')

                        if ereignis.state == 0:
                            self.speichern = False

                    if ereignis.code == 'BTN_TL2':
                        if ereignis.state == 1:
                            self.programm_ende = True
                            print('Programm beendet')

                    if ereignis.code == 'BTN_Z':
                        if ereignis.state == 1:
                            self.aufnahme = True
                            print('Aufnahme EIN')

                    if ereignis.code == 'BTN_WEST':
                        if ereignis.state == 1:
                            self.aufnahme = False
                            print('Aufnahme AUS')

                    if ereignis.code == 'BTN_EAST':
                        if ereignis.state == 1:
                            self.modus = "Manuell"
                            print('Manueller-Modus')

                    if ereignis.code == 'BTN_SOUTH':
                        if ereignis.state == 1:
                            self.modus = "Assistent"
                            print('Lenkasisstent-Modus')  

                    if ereignis.code == 'BTN_NORTH':
                        if ereignis.state == 1:
                            self.modus = "Automatik"
                            print('Autonomer-Modus') 