import requests
import urllib.parse
import os


class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def mk_dir(self, path):
        HEADERS = {'Authorization': f'OAuth {self.token}'}
        response = requests.put(
            'https://cloud-api.yandex.net/v1/disk/resources/',
            params={'path': path},
            headers=HEADERS
        )

    def upload_from_internet(self, url, path):
        HEADERS = {'Authorization': f'OAuth {self.token}'}
        response = requests.post(
            'https://cloud-api.yandex.net/v1/disk/resources/upload',
            params={'url': url, 'path': path},
            headers=HEADERS,
        )

    def get_upload_url(self, file_path: str):
        HEADERS = {'Authorization': f'OAuth {self.token}'}
        path = file_path
        response = requests.get(
            'https://cloud-api.yandex.net/v1/disk/resources/upload',
            params={'path': path, 'overwrite': 'true'},
            headers=HEADERS,
        )
        url = response.json()['href']
        return url

    def upload(self, url, file):
        upload = requests.put(url, data=file)
