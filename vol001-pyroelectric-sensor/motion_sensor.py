#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from time import sleep
import RPi.GPIO as GPIO

try:
    # GPIOを設定
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)

    start_datetime = datetime.now()

    while start_datetime + timedelta(seconds=30) > datetime.now():
        # GPIOの状態を取得
        detect = GPIO.input(18)
        print(detect)

        if detect == 1:
            print("人を検知")

        sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
