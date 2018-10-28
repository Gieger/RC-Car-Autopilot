# RC-Car-Autopilot
> Entwicklung eines Autopiloten für ein RC-Fahrzeug durch maschinelles lernen 



[![Python Version][PY-url]][Py-image]


![](./media/herbie_v2.png)

## Voraussetzungen 

Der Programmcode ist unter Ubuntu 16.04 getestet.

Um das Programm zu starten werden folgende Abhängigkeiten benötigt:

* Linux 16.04 LTS
* Python 3.x

```sh
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip

pip3 install opencv
```

## Installation

Das Repositorie clonen 

```sh
git clone https://github.com/Gieger/RC-Car-Autopilot.git
```

Starten der Software

```sh
sudo python3 herbie.py
```

## Nutzung

Die Software wird über das Gamepad gesteuert.


## Release History

* 0.1.0
    * Erste Fahrbereite Version
    * Änderungen: Modular aufgebaut
* 0.0.1
    * Start



Dennis Gieger 

[https://github.com/Gieger/](https://github.com/Gieger/)


<!-- Markdown link & img dfn's -->
[Py-image]: (https://img.shields.io/pypi/pyversions/donkeycar.svg)
[PY-url]: https://img.shields.io/badge/python-3.x-blue.svg
