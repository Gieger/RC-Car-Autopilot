
from car import Herbie
from parts.camera import USB_Camera as Camera
from parts.datastore import Datastore
from parts.controller import Logitech_F710 as Controller
#from parts.pilot import Pilot
from parts.pwm import PCA9685
from parts.webserver.server import WebServer

print('Herbie startet')
camera = Camera(resolution=(600,800),fps=30)
herbie = Herbie()
controller = Controller()
#pilot = Pilot()
datastore = Datastore()
pwm = PCA9685()
server = WebServer()

print('Komponenten laden...')

herbie.add(camera, outputs=['camera'], threaded=True)
herbie.add(controller, outputs=['speed','angle','record','mode','save','end'], threaded=True)
#car.add(pilot, inputs=['camera'], outputs=['pilot_steering'], threaded=True)
herbie.add(pwm, inputs=['speed','angle'], threaded=True)
herbie.add(datastore, inputs=['camera','speed','angle','record','save'], threaded=True)
herbie.add(server, inputs=['camera','speed','angle'],threaded=True)

herbie.start()



