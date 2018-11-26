from time import sleep
from datetime import datetime

import picamera


def photo():
    now_time = datetime.now()
    photo_name = 'image.taken_{0:%Y%m%d-%H%M%S}.jpg'.format(now_time)
    print(photo_name)

    with picamera.PiCamera() as camera:
        camera.resolution = (720, 480)
        camera.brightness = 50

        camera.start_preview()
        sleep(2)
        camera.capture(photo_name)
        camera.stop_preview()

    return photo_name
