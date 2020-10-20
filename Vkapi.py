import requests
from urllib.parse import urljoin


TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
V = '5.21'


class ApiVK:

    def __init__(self, user_id, token=TOKEN, v=V):
        self.base_url = 'https://api.vk.com/method/'
        self.token = token
        self.v = v
        self.user_id = user_id

    def get_albums(self):
        method = 'photos.getAlbums'
        params = {
            'access_token': self.token,
            'v': self.v,
            'owner_id': self.user_id,
            'need_system': '1'
        }
        response = requests.get(urljoin(self.base_url, method), params=params)
        albums = response.json()['response']['items']
        return albums

    def get_photos(self, album_id):
        params = {
            'access_token': self.token,
            'v': self.v,
            'owner_id': self.user_id,
            'album_id': album_id,
            'extended': '1',
            'photo_sizes': '1',
        }
        method = 'photos.get'
        response = requests.get(urljoin(self.base_url, method), params=params)
        photos = response.json()['response']['items']
        return photos

    def get_max_size(self, photo):
        size_type = ['w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 'm', 's']
        for typ in size_type:
            for size in photo['sizes']:
                if typ in size['type']:
                    return [size['src'], size['type']]

    def get_photos_info(self, albums):
        album_info = dict()
        for album in albums:
            album_id = album['id']
            album_title = album['title']
            album_info[album_title] = []
            for photo in self.get_photos(album_id):
                photo_info = []
                name = photo['likes']['count']
                names = [item[0] for item in album_info[album_title]]
                if (str(name) + '.jpg') in names:
                    name = str(name) + '(' + str(photo['date']) + ')'
                photo_info.append(str(name) + '.jpg')
                photo_info.append(self.get_max_size(photo)[0])
                photo_info.append(self.get_max_size(photo)[1])
                album_info[album_title].append(photo_info)
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
