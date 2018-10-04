
from car import Vehicle
from parts.camera import USB_Camera as Camera
#from parts.datastore import Datastore
#from parts.controller import Xbox_F710 as Controller
#from parts.pilot import Pilot
#rom parts.pwm import PCA9685
from parts.webserver.server import WebServer

camera = Camera(resolution=(600,800),fps=30)
#controller = Controller()
#pilot = Pilot()
#datastore = Datastore()
#pwm = PCA9685()
server = WebServer()
car = Vehicle()
print('Parts laden...')
car.add(camera, outputs=['camera'], threaded=True)
#car.add(controller, outputs=['controller'], threaded=True)
car.add(server, inputs=['camera','controller'],threaded=True)
#car.add(pilot, inputs=['camera'], outputs=['pilot_steering'], threaded=True)
#car.add(pwm, inputs=['controller','pilot_steering'], threaded=True)
#car.add(datastore, inputs=['camera','controller'], threaded=True)

car.start()
car.update_parts()
#car.stop()


