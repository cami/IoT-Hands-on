#! /usr/bin/python
# -*- coding: utf-8 -*-

# python3 motion_sensor.py

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

sleep(1)

try:
	for num in range(0,29):
		motion = GPIO.input(18)
		print(motion)
		if motion == 1:
			print("人を検知")
		sleep(1)
		
except KeyboardInterrupt:
	print("\nCtrl + C")

GPIO.cleanup()

