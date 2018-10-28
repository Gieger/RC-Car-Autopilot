# farhzeug.py
# Author: Dennis Gieger

# Bibliotheken import
from threading import Thread
import random
import time

# Klasse repräsentiert den Speicher
class Speicher():

	# Speicher initialisierung
    def __init__(self):
        self.woerterbuch = {}
        pass
    
	# Methode zum Schreiben in den Speicher
    def schreiben(self, name, eingang):
        if len(name) > 1:
            for i, wert in enumerate(name):
                    self.woerterbuch[wert] = eingang[i]

        else:
            self.woerterbuch[name[0]] = eingang
			
	# Methode zum lesen aus dem Speicher
    def lesen(self, name):
        ausgang = [self.woerterbuch.get(k) for k in name]
        return ausgang 

		
"""
Das Schema einer neuen Komponente als Thread ist:

	class Komponente():
		name = "Komponenten_name"
		
		def __init__(self):
			Initalisierung
		 
		def ausfuehren_parallel(self):
			Parallel ausgeführter Code

		def aktualisieren(self):
			Ein- und Ausgabe in die Hauptschleife

		def beenden(self):
			Komponente beenden

Das Schema einer neuen Komponente ohne Thread ist:

	class Komponente():
		name = "Komponenten_name"
		
		def __init__(self):
			Initalisierung
		 
		def ausfuehren(self):
			Ausgeführter Code
			Ein- und Ausgabe in die Hauptschleife

		def beenden(self):
			Komponente beenden
"""	
	
# Klasse repräsentiert das Fahrzeug
class Herbie():

	# Fahrzeug initialisierung
    def __init__(self, speicher=None):
        speicher = Speicher()
        self.speicher = speicher
        self.programm_laeuft = True
        self.komponenten = []
     
	# Methode zum Komponenten hinzfügen
    def hinzufuegen(self, komponente, eingang=[], ausgang=[], ausfuehren_parallel=False):    
        p = komponente
        print('Komponente hinzufügen {}.'.format(p.name))
        eintrag={}
        eintrag['komponente'] = p
        eintrag['eingang'] = eingang
        eintrag['ausgang'] = ausgang
        
        if ausfuehren_parallel:
            t = Thread(target=komponente.aktualisieren, args=())
            t.daemon = True
            eintrag['thread'] = t
        
        self.komponenten.append(eintrag)
    
	# Methode zum Komponenten starten
    def starten(self, geschwindigkeit_hz=0.1, max_schleifen_anzahl=None):
        self.programm_laeuft = True

        for eintrag in self.komponenten:
            if eintrag.get('thread'):
                eintrag.get('thread').start()

        print('Fahrzeug wird gestartet...')

        schleifen_zähler = 0

        while self.programm_laeuft:
            schleifen_zähler += 1

            self.aktualisieren()
            
            time.sleep(geschwindigkeit_hz)

            if max_schleifen_anzahl and schleifen_zähler > max_schleifen_anzahl:
                self.programm_laeuft = False
                self.anhalten()
				
	# Methode zum Komponenten aktualisieren
    def aktualisieren(self):
        for eintrag in self.komponenten:
            p = eintrag['komponente']

            eingang = self.speicher.lesen(eintrag['eingang'])

            if eintrag.get('thread'):
                ausgang = p.ausfuehren_parallel(*eingang)
            else:
                ausgang = p.run(*eingang)
            if ausgang is not None:
                self.speicher.schreiben(eintrag['ausgang'], ausgang)

	# Methode zum Komponenten beenden
    def beenden(self):
        for eintrag in self.komponenten:
            eintrag['komponente'].beenden()




