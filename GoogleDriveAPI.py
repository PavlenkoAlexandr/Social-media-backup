from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import requests

class GoogleApi:

    SCOPES = ['https://www.googleapis.com/auth/drive']
    CLIENT_SECRET = 'client_secret.json'

    store = file.Storage('storage.json')
    credz = store.get()
    if not credz or credz.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
        credz = tools.run_flow(flow, store)

    SERVICE = build('drive', 'v3', http=credz.authorize(Http()))

    def make_dir(self, name, parents=[]):
        file_metadata = {
            'parents': parents,
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        self.SERVICE.files().create(
            body=file_metadata,
            fields='id'
        ).execute()

    def get_id(self, name):
        response = self.SERVICE.files().list(
            q=f'name="{name}"',
            fields='files(id)',
        ).execute()
        for file in response.get('files', []):
            return file.get('id')

    def files_list(self):
        response = self.SERVICE.files().list(
            q='',spaces='',
            fields='nextPageToken, files(id, name)',
        ).execute()
        for file in response.get('files', []):
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))

    def upload_file(self, name, path, parents=[]):
        file_metadata = {
            'name': name,
            'parents': parents,
        }
        media = MediaFileUpload(path)
        file = self.SERVICE.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
        ).execute()

    def upload_from_internet(self, url, name, parents=[]):
        file = requests.get(url)
        with open(name, 'wb') as f:
            f.write(file.content)
        self.upload_file(name=name, path=name, parents=parents)
        os.remove(name)
