from inputs import get_gamepad


class Logitech_F710():
    name = "Gamepad"
    def __init__(self):

        self.events = None
        self.speed = 0
        self.angle = 0
        self.record = False
        self.mode = "User"
        self.end = False
        self.save = False
        self.on = True

        print('Controller loading')

    def run_threaded(self):
        return self.speed, self.angle, self.record, self.mode, self.save, self.end

    def update(self):
        self.running=True
        while self.running:
            self.events = get_gamepad()

            for event in self.events:
                #print(event.ev_type, event.code, event.state)
                if event.ev_type == 'Absolute':
                    
                    if event.code == 'ABS_Y':
                        val = event.state
                        if val == 255:
                            self.speed = float(0)
                        if val > 255:
                            self.speed = float(val / 32767)
                        if val < -255:
                            self.speed = float(val / 32768)
                        print(self.speed)

                    elif event.code == 'ABS_RX':
                        if event.state == 0:
                            self.angle = float(0)
                        if event.state > 0:
                            self.angle = float(event.state / 32767)
                        if event.state < 0:
                            self.angle = float(event.state / 32768)
                        print(self.angle)

                if event.ev_type == 'Key':  

                    if event.code == 'BTN_START':
                        if event.state == 1:
                            self.save = True
                            print('Save')

                        if event.state == 0:
                            self.save = False
                            print('Save')

                    if event.code == 'BTN_SELECT':
                        if event.state == 1:
                            self.end = True
                            print('Programm ENDE')

                    if event.code == 'BTN_TR':
                        if event.state == 1:
                            self.record = True
                            print('Record ON')

                    if event.code == 'BTN_TL':
                        if event.state == 1:
                            self.record = False
                            print('Record OFF')

                    if event.code == 'BTN_SOUTH':
                        if event.state == 1:
                            self.mode = "User"
                            print('Benutzer-Modus')

                    if event.code == 'BTN_NORTH':
                        if event.state == 1:
                            self.mode = "Assist"
                            print('Lenkasisstent-Modus')  

                    if event.code == 'BTN_WEST':
                        if event.state == 1:
                            self.mode = "Assist"
                            print('Autonomesfahren-Modus') 

            #if not self.on:
                #break

    def shutdown(self):
        self.on = False
        print('stoping Gamepad')
        time.sleep(.5)


class Xbox_F710():
    name = "Gamepad"

    def __init__(self):
        self.events = None
        self.speed = 0
        self.angle = 0
        self.record = False
        self.mode = False
        self.save = False
        self.end
        self.on = True
        print('Controller loading')

    def run_threaded(self):
        return self.speed, self.angle, self.record, self.end, self.save, self.mode

    def update(self):
        self.running = True
        while self.running:
            self.events = get_gamepad()

            for event in self.events:
                #print(event.ev_type, event.code, event.state)
                if event.ev_type == 'Absolute':

                    if event.code == 'ABS_Y':
                        if event.state == 127:
                            self.speed = float(0)
                        if event.state > 127:
                            self.speed = float((event.state - 127) / 128)
                        if event.state < 127:
                            self.speed = float((event.state - 127) / 127)
                        #print(self.speed)


                    elif event.code == 'ABS_Z':
                        if event.state == 128:
                            self.angle = float(0)
                        if event.state > 128:
                            self.angle = float((event.state - 128) / 127)
                        if event.state < 128:
                            self.angle = float((event.state - 128) / 128)
                        #print(self.angle)


                if event.ev_type == 'Key':

                    if event.code == 'BTN_START':
                        if event.state == 1:
                            self.save = True
                            print('Save')

                        if event.state == 0:
                            self.save = False
                            print('Save')

                    if event.code == 'BTN_SELECT':
                        if event.state == 1:
                            self.end = True
                            print('Stop All')

                    if event.code == 'BTN_TR':
                        if event.state == 1:
                            self.record = True
                            print('Record ON')

                    if event.code == 'BTN_TL':
                        if event.state == 1:
                            self.record = False
                            print('Record OFF')

                    if event.code == 'BTN_SOUTH':
                        if event.state == 1:
                            self.mode = "User"
                            print('Assist OFF')

                    if event.code == 'BTN_NORTH':
                        if event.state == 1:
                            self.mode = "Assist"
                            print('Assist ON')

                    if event.code == 'BTN_EAST':
                        if event.state == 1:
                            self.mode = "Auto"
                            print('Assist ON')

                    # if not self.on:
                    #    break

    def shutdown(self):
        self.on = False
        print('stoping Gamepad')
        time.sleep(.5)