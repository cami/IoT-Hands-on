#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from time import sleep
import datetime
import yaml

import RPi.GPIO as GPIO
import picamera
import requests


# Raspberry Pi の GPIO を起動
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
sleep(2)

try:
    # 撮影した写真をslackに送信
    with open('config.yml', 'r') as config_in_yml:
        config = yaml.load(config_in_yml)
        url = config['url']
        slack_config = {
            'token': config['token'],
            'channels': config['channels'],
            'initial_comment': config['initial_comment']
        }

    while True:
        detected = GPIO.input(18)
        print(detected)

        if detected == 1:
            # 焦電センサが動体を感知したら、PiCameraを起動して写真撮影
            print('動体を検知。写真を撮影します。')
            now_time = datetime.datetime.now()
            print(now_time)
            image_name = 'motion.captured_{0:%Y%m%d-%H%M%S}.png'.format(now_time)
            print(image_name)

            with picamera.PiCamera() as camera:
                camera.hflip = True
                camera.vflip = True
                camera.resolution = (1024, 768)
                camera.capture(image_name)
                print('captured')

                print('requesting')
                with open(image_name, 'rb') as f:
                    slack_config['filename'] = image_name
                    requests.post(url, params=slack_config, files={'file': f})
                print('requests complete')

            print('Delete the image')
            Path(image_name).unlink()

        sleep(1)

except KeyboardInterrupt:
    print("\nCtrl + C により検出が停止されました。")

finally:
    GPIO.cleanup()
