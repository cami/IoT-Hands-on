from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
from pathlib import Path
import argparse
import mimetypes
import sys


class Drive:
    CREDENTIAL_DIR_PATH = '../../credentials'
    SCOPES = 'https://www.googleapis.com/auth/drive.file'

    def __init__(self):
        pass

    def authorize(self):
        credential_dir = Path(__file__).parent / self.CREDENTIAL_DIR_PATH

        store = file.Storage(str(credential_dir / 'token.json'))
        credentials = store.get()

        if not credentials or credentials.invalid:
            print('Create google api credentials')

            flow = client.flow_from_clientsecrets(str(credential_dir / 'credentials.json'), self.SCOPES)
            parser = argparse.ArgumentParser(parents=[tools.argparser])
            argv = [*sys.argv[1:], '--noauth_local_webserver']  # コマンドライン引数に追加する
            credentials = tools.run_flow(flow, store, parser.parse_args(argv))

            print('Authenticated google api')

        self.service = build('drive', 'v3', http=credentials.authorize(Http()))

    def upload_file(self, file_path, folder_id):
        print('uploading')

        res = self.service.files().create(
            body={
                'name': Path(file_path).name,
                'parents': [folder_id]
            },
            media_body=MediaFileUpload(file_path, mimetype=mimetypes.guess_type(file_path), resumable=True)
        ).execute()

        print('Successfully Uploaded! https://drive.google.com/open?id={}'.format(res['id']))
