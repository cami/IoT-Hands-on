#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from time import sleep
import datetime

import RPi.GPIO as GPIO
import picamera
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

# Slackの設定情報
SLACK_URL = 'https://slack.com/api/files.upload'
SLACK_CONFIG = {
    'token': "xoxp-",
    'channels': "security-camera",
    'filename': "https://slack.com/api/files.upload",
    'initial_comment': "Upload Suspicious Person"
}

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()

        while True:
            detect = GPIO.input(18)
            print(detect)

            # 人を検知した
            if detect == 1:
                print("人を検知したため、写真を撮影しました。")

                now_time = datetime.datetime.now()
                print(now_time)

                image_path = Path(f"motion.captured_{now_time:%Y%m%d-%H%M%S}.png")
                print(image_path)

                # PiCameraで撮影を行う
                camera.capture(image_path)

                # 撮影した写真をSlackに送信する
                with image_path.open('rb') as f:
                    requests.post(SLACK_URL, params=SLACK_CONFIG, files={'file': f})

                # pngファイルを削除
                image_path.unlink()

            sleep(1)


except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
