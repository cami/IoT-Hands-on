#! /usr/bin/python python3.6
# -*- coding: utf-8 -*-

# python3 main.py で実行

import os
from time import sleep
import datetime

# ラズパイのGPIOを制御するためのmoduleをimport
import RPi.GPIO as GPIO
# PiCameraを操作するためのmoduleをimport
import picamera
# HTTP通信のためのmoduleをimport
import requests

# 撮影した写真のアップロード先のslackの情報
TOKEN = 'xoxp-'
CHANNEL = 'security-camera'
URL = 'https://slack.com/api/files.upload'


# def __init__(self, image_name, file):
#     self.image_name = image_name
#     self.file = file

# ラズパイのGPIOの初期設定
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)
    sleep(2)


# 焦電センサが人を感知したら、PiCameraを起動
def photo_taker():
    print("人を検知。写真を撮影します。")
    now_time = datetime.datetime.now()
    print(now_time)
    image_name = 'motion.captured_{0:%Y%m%d-%H%M%S}.png'.format(now_time)
    print(image_name)

    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        sleep(2)
        print("capturing")
        camera.capture(image_name)
        camera.stop_preview()
        print("captured")
        return image_name, {'file': open(image_name, 'rb')}


# 撮影した写真をslackに送信
def slack_notification(filename, file):
    payload = {
        'token': TOKEN,
        'channels': CHANNEL,
        'filename': filename,
        'initial_comment': "Upload Suspicious Person"
    }
    print("requesting")
    # 撮影した写真をslackに送信
    requests.post(URL, params=payload, files=file)
    print("deleting")
    os.remove(filename)


if __name__ == '__main__':
    setup()
    while True:
        motion = GPIO.input(18)
        print(motion)
        if motion == 1:
            filename, photo = photo_taker()
            slack_notification(filename, photo)
        sleep(1)
    GPIO.cleanup()
