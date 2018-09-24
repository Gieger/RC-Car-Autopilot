from car import Vehicle
from camera import USB_Camera as Camera
from datastore import Datastore
from controller import Logitech_F710 as Controller


camera = Camera(resolution=(600,800),fps=30)
controller = Controller()
datastore = Datastore()

car = Vehicle()

car.add(camera, outputs=['camera'], threaded=True)
car.add(controller, outputs=['controller'], threaded=True)
car.add(datastore, inputs=['camera','controller'], threaded=True)

car.start()
car.update_parts()

