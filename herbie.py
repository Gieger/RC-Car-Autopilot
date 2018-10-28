# herbie.py
# Author: Dennis Gieger

# Komponenten import
from fahrzeug import Herbie
from komponenten.steuerung import Xbox_F710 as Steuerung
from komponenten.kamera import PiCamera as Kamera
from komponenten.gyro import Mpu6050 as Gyroskope
from komponenten.pilot import Fahrer
from komponenten.pwm import PCA9685
from komponenten.datenspeicher import Datenspeicher
from komponenten.webserver.server import WebServer

print('Herbie startet')

# Instanziierung der Kopmponenten
herbie = Herbie()
steuerung = Steuerung()
kamera = Kamera()
gyro = Gyroskope()
fahrer = Fahrer()
pwm = PCA9685()
datenspeicher = Datenspeicher()
server = WebServer()

print('Komponenten laden...')

"""
Komponenten werden nach dem fogendem Schema angelegt:
	herbie.hinzufuegen(komponente, eingang=['eingang_name',...], ausgang=['ausgang_name',...], ausfuehren_parallel = True or False)
"""

# Hinzufügen der Komponenten
herbie.hinzufuegen(steuerung, ausgang=['beschleunigung','lenkung','aufnahme','modus','speichern','programm_ende'], ausfuehren_parallel=True)
herbie.hinzufuegen(kamera, ausgang=['kamera'], ausfuehren_parallel=True)
herbie.hinzufuegen(gyro, ausgang=['besch_x','besch_y','besch_z','gyro_x','gyro_y','gyro_z'], ausfuehren_parallel=True)

herbie.hinzufuegen(fahrer, eingang=['kamera','beschleunigung','lenkung','modus'], ausgang=['lenkung','beschleunigung'], ausfuehren_parallel=True)

herbie.hinzufuegen(pwm, eingang=['beschleunigung','lenkung'], ausfuehren_parallel=True)
herbie.hinzufuegen(datenspeicher, eingang=['kamera','beschleunigung','lenkung','aufnahme','speichern','besch_x','besch_y','besch_z','gyro_x','gyro_y','gyro_z'], ausfuehren_parallel=True)
herbie.hinzufuegen(server, eingang=['kamera','beschleunigung','lenkung'],ausfuehren_parallel=True)

# Hauptschleife starten
herbie.starten()