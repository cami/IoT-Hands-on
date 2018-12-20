#!/usr/bin/env python3

from PIL import Image
from datetime import datetime
from pathlib import Path
from processor import configparser
from processor import transcoder
from processor.camera import Camera
from processor.detector import PersonDetector
from processor.slack import Slack
from processor.trigger import GpioTrigger
import cv2
import io
import numpy as np
import time


def main():
    config = configparser.load()

    slack = Slack(config['slack_token'], config['slack_channel'])

    trigger = GpioTrigger()
    trigger.start()

    camera = Camera()
    camera.start()

    person_detector = PersonDetector(str(Path(__file__).parent / config['opencv_classifier_name']))

    try:
        while True:
            # if not trigger.detect():
            #     continue

            print('動体を検知しました。分析にかけます')

            # 画像を解析する
            stream = camera.take_photo()
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)
            faces = person_detector.identifier(image)

            # Slackに送るコメントを作成
            if len(faces) > 0:
                comment = '人物を検知！写真を送ります'
            else:
                comment = '動体を検知しましたが人物ではありませんでした'

            print(comment)

            # Slackに画像をアップロードする
            person_detector.marking(image, faces)
            imgBytesIO = io.BytesIO()
            Image.fromarray(image).save(imgBytesIO, format='PNG')
            slack.files_upload(comment, imgBytesIO.getvalue(), datetime.now().isoformat())

            # Slackに動画をアップロードする
            # slack.files_upload(comment, transcoder.transcode(camera.record_video()), datetime.now().isoformat() + '.h264')

            print('Slackへ通知しました')

            time.sleep(1)

    except KeyboardInterrupt:
        print('動体検知が終了しました')

    finally:
        trigger.stop()
        camera.stop()


if __name__ == '__main__':
    main()
