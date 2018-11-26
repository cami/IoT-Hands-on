from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools
import argparse


class UploadGoogleDrive:
    def __init__(self):
        SCOPES = 'https://www.googleapis.com/auth/drive.file'
        CREDENTIAL_PATH = '/home/pi/IoT-Hands-on/vol002-surveillance-camera/credentials/credentials.json'
        TOKEN_PATH = '/home/pi/IoT-Hands-on/vol002-surveillance-camera/credentials/token.json'

        store = file.Storage(TOKEN_PATH)
        credentials = store.get()

        if not credentials or credentials.invalid:
            print('credentials')
            parser = argparse.ArgumentParser(parents=[tools.argparser])
            flags = parser.parse_args()
            flow = client.flow_from_clientsecrets(CREDENTIAL_PATH, SCOPES)
            credentials = tools.run_flow(flow, store, flags)
            print('authenticated')
        self.service = build('drive', 'v3', http=credentials.authorize(Http()))

    def upload_movie(self, movie_name):
        FOLDER_ID = ''
        file_metadata = {
            'name': movie_name,
            'parents': [FOLDER_ID]
        }
        media = MediaFileUpload(movie_name, mimetype='video/h264', resumable=True)

        print('uploading')
        self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        print('Successfully Uploaded!')
