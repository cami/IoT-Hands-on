from slackclient import SlackClient


class Slack:
    def __init__(self, token, channel=''):
        self.slack = SlackClient(token)
        self.channel = channel

    def files_upload(self, comment, file, filename, channels=None):
        """
        ファイルをアップロードする
        :param comment:
        :param file:
        :param channels:
        """
        res = self.slack.api_call(
            'files.upload',
            channels=','.join(channels or [self.channel]),
            filename=filename,
            initial_comment=comment,
            file=file
        )
        self._validate_response(res)

    def chat_post_message(self, text, channel=None):
        """
        メッセージを投稿する
        :param text:
        :param channel:
        """
        res = self.slack.api_call(
            'chat.postMessage',
            channel=channel or self.channel,
            text=text
        )
        self._validate_response(res)

    @staticmethod
    def _validate_response(res):
        if not res['ok']:
            raise Exception('Slack message is not sended: {}'.format(res['error']))
