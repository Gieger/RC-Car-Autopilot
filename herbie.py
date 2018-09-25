from car import Vehicle
from parts.camera import USB_Camera as Camera
from parts.datastore import Datastore
from parts.controller import Xbox_F710 as Controller
from parts.pwm import PCA9685

camera = Camera(resolution=(600,800),fps=30)
controller = Controller()
datastore = Datastore()
pwm = PCA9685()

car = Vehicle()

car.add(camera, outputs=['camera'], threaded=True)
car.add(controller, outputs=['controller'], threaded=True)
car.add(pwm, inputs=['controller'], threaded=True)
car.add(datastore, inputs=['camera','controller'], threaded=True)
print('Car Create')
car.start()
car.update_parts()
#car.stop()


