import requests
from hashlib import md5
import datetime

application_id = ''
application_key = ''
token = ''
secret_session_key = ''
api_url = 'https://api.ok.ru/fb.do'


def get_date(time):

    date = datetime.datetime.fromtimestamp(int(time))
    return str(date).replace(':', '-').replace(' ', '_')


class OkApi:

    def __init__(
            self,
            application_key=application_key,
            token=token,
            secret_session_key=secret_session_key
    ):
        self.application_key = application_key
        self.token = token
        self.secret_session_key = secret_session_key

    def get_sig(self, params):

        keys = sorted(params.keys())
        signature = ''.join(['{k}={v}'.format(k=key, v=params[key]) for key in keys])
        signature += self.secret_session_key
        sig = md5(signature.encode('utf-8')).hexdigest().lower()
        return sig

    def params_update(self, params):

        sig = self.get_sig(params)
        params.update({
            'access_token': self.token,
            'sig': sig
        })

    def get_photos(self, id=''):

        params = {
            'fields': 'photo.CREATED_MS, photo.PIC_MAX, photo.LIKE_COUNT, photo.STANDARD_HEIGHT, photo.STANDARD_WIDTH',
            'format': 'json',
            'method': 'photos.getPhotos',
            'aid': id,
            'application_key': self.application_key,
        }
        self.params_update(params)
        response = requests.get(api_url, params=params)
        return response.json()['photos']

    def get_albums(self):

        params = {
            'application_key': self.application_key,
            'format': 'json',
            'method': 'photos.getAlbums'
        }
        self.params_update(params)
        response = requests.get(api_url, params=params)
        albums = [[item['aid'], item['title']] for item in response.json()['albums']]
        return albums

    def get_one_photo_info(self, photo, album_title):

        photo_info = list()
        name = photo['like_count']
        names = [item[0] for item in album_title]
        if (str(name) + '.jpg') in names:
            name = str(name) + f'({get_date(str(photo["created_ms"])[:-3])})'
        photo_info.append(str(name) + '.jpg')
        photo_info.append(str(photo['pic_max']))
        photo_info.append(f'{photo["standard_width"]}x{photo["standard_height"]}')
        return photo_info

    def get_photos_info(self, albums):

        album_info = dict()
        for album in albums:
            album_info[album[1]] = list()
            for photo in self.get_photos(album[0]):
                photo_info = self.get_one_photo_info(photo, album_info[album[1]])
                album_info[album[1]].append(photo_info)
        album_info['Фотографии из личного альбома'] = list()
        for photo in self.get_photos():
            photo_info = self.get_one_photo_info(photo, album_info['Фотографии из личного альбома'])
            album_info['Фотографии из личного альбома'].append(photo_info)
        return album_info

    def get_photos_log(self, info):
        log = list()
        for value in info.values():
            for photo in value:
                upload_log = dict()
                upload_log['file_name'] = photo[0]
                upload_log['size'] = photo[2]
                log.append(upload_log)
        return log
