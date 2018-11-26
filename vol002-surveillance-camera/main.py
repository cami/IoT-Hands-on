#! /usr/bin/env python3

# python3 main.py --noauth_local_webserver で実行

from time import sleep
import RPi.GPIO as GPIO
import os
import glob

# 焦電センサを使うならば photo, person_identifier を import する
from processor.Photo import photo
from processor.PersonIdentifier import person_identifier

# picamera で完結させるならば、CircularIO, UploadGoogleDrive を import する
# from processor.CircularIO import CircularIO
# from processor.UploadGoogleDrive import UploadGoogleDrive

from processor.SlackNotification import SlackNotification


def main():
    slack_notification = SlackNotification()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)
    sleep(2)
    GPIO.add_event_detect(18, GPIO.RISING)

    # photo, person_identifier を import した場合、コメントアウトを外す
    # CircularIO, UploadGoogleDrive を import した場合、コメントアウト
    try:
        while True:
            if GPIO.event_detected(18):
                print('動体を検知しました。分析にかけます。')

                photo_name = photo()
                num_faces, filename = person_identifier(photo_name)

                with open(filename, 'rb') as f:
                    if num_faces >= 1:
                        photo_comment = '人物を検知！写真を送ります。'
                    else:
                        photo_comment = '動体を検知しましたが人物ではありませんでした。'

                    print(photo_comment)

                    slack_notification.upload_file(filename, photo_comment, f)

    # photo, person_identifier を import した場合、コメントアウト
    # CircularIO, UploadGoogleDrive を import した場合、コメントアウトを外す
    # upload_google_drive = UploadGoogleDrive()
    # circular_io = CircularIO()
    #
    # print('エッジイベント検出中')
    #
    # try:
    #     while True:
    #         if GPIO.event_detected(18):
    #             movie_name = circular_io.movie()
    #
    #             movie_comment = 'イベント録画を行いました。動画を送信します。'
    #             slack_notification.send_message(movie_comment)
    #             sleep(3)
    #             upload_google_drive.upload_movie(movie_name)
    #             sleep(5)

    except KeyboardInterrupt:
        print('\nCtrl + C により、動体検知が終了しました。')

    finally:
        for p in glob.glob('*.jpg', recursive=True):
            if os.path.isfile(p):
                os.remove(p)

        for p in glob.glob('*.h264', recursive=True):
            if os.path.isfile(p):
                os.remove(p)

    print('deleted unnecessary files :)')

    GPIO.remove_event_detect(18)

    # photo, person_identifier を import した場合、コメントアウト
    # CircularIO, UploadGoogleDrive を import した場合、コメントアウトを外す
    # circular_io.camera_cleanup()


if __name__ == '__main__':
    main()
