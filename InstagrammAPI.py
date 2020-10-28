import requests


class InstagramAPI:

    def __init__(self, token):
        self.token = token

    def get_photo(self):
        response = requests.get('https://graph.instagram.com/me/media', params={
            'fields': 'id,media_type,media_url,username,timestamp',
            'access_token': self.token
        })
        return response.json()['data']

    def get_photo_from_album(self, id):
        response = requests.get(f'https://graph.instagram.com/{id}/children', params={
            'fields': 'id,media_type,media_url,username,timestamp',
            'access_token': self.token
        })
        return response.json()['data']

    def get_photos_info(self):
        photos_info = list()
        for photo in self.get_photo():
            if photo['media_type'] == 'IMAGE':
                name = photo['timestamp'].split("+")[0].replace(':', '-')
                url = photo['media_url']
                photos_info.append([name, url])
            elif photo['media_type'] == 'CAROUSEL_ALBUM':
                for album_photo in self.get_photo_from_album(photo['id']):
                    if album_photo['media_type'] == 'IMAGE':
                        name = album_photo['timestamp'].split('+')[0].replace(':', '-')
                        names = [item[0] for item in photos_info]
                        n = 1
                        while name in names:
                            name = name.split('(')[0]
                            name += f'({str(n)})'
                            n += 1
                        url = album_photo['media_url']
                        photos_info.append([name, url])
        return photos_info

    def get_photos_log(self, info):
        log = list()
        for photo in info:
            upload_log = dict()
            upload_log['file_name'] = photo[0]
            log.append(upload_log)
        return log
