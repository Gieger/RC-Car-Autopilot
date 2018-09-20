
# Evdev importieren
from evdev import InputDevice, categorize, ecodes, KeyEvent

# Input Device zuweisen, event0 kann abweichen und muss dann hier geändert werden
dev = InputDevice('/dev/input/event1')

# Ausgabe Input Device
print(dev)

# Schleife zur Ausgabe der Werte bei betätigung der Button ode Analog-Sticks
try:
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            print(categorize(event))
            keyevent = categorize(event)
            print (keyevent.keycode)
        if event.type == ecodes.EV_ABS:
            print(categorize(event))
            keyevent = categorize(event)
            print (event.value)

except IOError:
    print("error")

"""
#import evdev
from evdev import InputDevice, categorize, ecodes

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event0')

#prints out device info at start
print(gamepad)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    #filters by event type
    if event.type == ecodes.EV_KEY:
        print(event)"""