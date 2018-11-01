#! /usr/bin/python
# -*- coding: utf-8 -*-

# python3 motion_detected_send_slack.py

import os
import glob
from time import sleep
import datetime

# ラズパイのGPIOを制御するためのmoduleをimport
import RPi.GPIO as GPIO
# PiCameraを操作するためのmoduleをimport
import picamera
# HTTP通信のためのmoduleをimport
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

# 撮影した写真のアップロード先の情報
TOKEN = 'xoxp-'
CHANNEL = 'security-camera'
URL = 'https://slack.com/api/files.upload'

sleep(2)

try:
	while True:
		motion = GPIO.input(18)
		print(motion)

		# 人を検知した場合に実行
		if motion == 1:
			print("人を検知。写真を撮影しました。")
			now_time = datetime.datetime.now()
			print(now_time)
			image_name = 'motion.captured_{0:%Y%m%d-%H%M%S}.png'.format(now_time)
			print(image_name)

			# PiCameraで撮影を行う
			with picamera.PiCamera() as camera:
				camera.resolution = (1024, 768)
				camera.capture(image_name)
				files = {'file': open(image_name, 'rb')}
				payload = {
					'token': TOKEN,
					'channels': CHANNEL,
					'filename': image_name,
					'initial_comment': "Upload Suspicious Person"
				}
				# 撮影した写真をslackに送信
				requests.post(URL, params=payload, files=files)

				# pngファイルを削除
				os.remove(image_name)

		sleep(1)

except KeyboardInterrupt:
	print("\nCtrl + C")

GPIO.cleanup()
