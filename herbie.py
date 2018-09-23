from car import Vehicle
from camera import USB_Camera as Camera
from datastore import Datastore


camera = Camera(resolution=(600,800),fps=30)
datastore = Datastore()

car = Vehicle()

car.add(camera, outputs=['camera'], threaded=True)
car.add(datastore, inputs=['camera'])

car.start()
car.update_parts()

