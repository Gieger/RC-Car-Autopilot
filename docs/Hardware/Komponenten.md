### Blockschaltbild

![](../media/abbildung1.PNG)
Abbildung 1

### Erläuterung zu Abbildung 1:

Im folgendem wird ein Überblick über die Hardware Vernetzung gegeben

**Kamera und Controller**

Diese sind über den USB-Port an den Raspberry Pi als Eingabegeräte
angeschlossen.

**Raspberry Pi**

Hier werden die Signale angenommen und weiterverarbeitet. Die Signale des
Controllers werden über den IC2 Bus an das PWM-Bord weitergeleitet.

**PWM-Bord**

Wandelt die IC2 Signale in ein PWM Signal um und leitet die Signale an den
Fahrtenregler Sowie den Lenkservo weiter.

**Fahrtenregler**

Es werden die PWM Signale angenommen und entsprechend der Laststromkreis für den
Motor geregelt.

**Motor**

Wird über die Regelung des Fahrtenreglers mit Strom versorgt.

**Lenkservo**

Nimmt die Signale des PWM-Boards entgegen und leitet den Strom an den Lenkservo
weiter.
