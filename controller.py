from inputs import get_gamepad

class Logitech_F710():
    name = "Gamepad"
    def __init__(self):
        self.events = None
        self.speed = 0
        self.angle = 0
        self.record = False
        self.stop_all = False
        self.save = False

        self.on = True

    def run_threaded(self):
        return self.speed, self.angle, self.record, self.stop_all, self.save

    def update(self):
        self.running=True
        while self.running:
            self.events = get_gamepad()

            for event in self.events:
                #print(event.ev_type, event.code, event.state)
                if event.ev_type == 'Absolute':
                    
                    if event.code == 'ABS_Y':
                        self.speed = event.state
                        #print(event.state)

                    if event.code == 'ABS_X':
                        self.angle = event.state
                        #print(event.state)

            if event.ev_type == 'key':  

                if event.code == 'BTN_SOUTH':
                    self.record = True    

            #if not self.on:
            #    break

    def shutdown(self):
        self.on = False
        print('stoping Gamepad')
        time.sleep(.5)
