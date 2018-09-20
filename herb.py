from gamepad import Controller


def gen(controller):
    while True:
        steering = controller.get_key()
        print(steering)



gen(Controller())