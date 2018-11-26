#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

"""
撮影した写真のアップロード先のslackの情報
:param filename:
:param comment:
:param file:
:return:
"""


class SlackNotification:
    def __init__(self):
        self.TOKEN = ''
        self.CHANNEL = 'CDSC8F066'

    # 撮影した写真のアップロード先のslackの情報
    def upload_file(self, filename, photo_comment, f):
        URL = 'https://slack.com/api/files.upload'
        slack_config = {
            'token': self.TOKEN,
            'channels': self.CHANNEL,
            'filename': filename,
            'initial_comment': photo_comment
        }

        print('requesting')
        res = requests.post(URL, params=slack_config, files={'file': f})
        print(res)
        print('Slack への通知が完了しました。')

    # メッセージの送信先のslackの情報
    def send_message(self, movie_comment):
        URL = 'https://slack.com/api/chat.postMessage'
        slack_config = {
            'token': self.TOKEN,
            'channels': self.CHANNEL,
            'text': movie_comment,
        }

        print('requesting')
        res = requests.post(URL, params=slack_config)
        print(res)
        print('一連の手続きが完了しました。')
