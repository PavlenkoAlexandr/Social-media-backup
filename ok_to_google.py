import okApi
import GoogleDriveAPI
import tqdm
import json


def run():

    application_key = input('Введите application key вашего приложения: ')
    token = input('Введите ваш токен доступа: ')
    secret_session_key = input('Введите ваш secret session key: ')

    okapi = okApi.OkApi(application_key, token, secret_session_key)
    g = GoogleDriveAPI.GoogleApi()

    all_photos = okapi.get_photos_info(okapi.get_albums())
    log = okapi.get_photos_log(all_photos)

    g.make_dir('ok')
    ok_dir_id = g.get_id('ok')

    for key, value in all_photos.items():
        g.make_dir(key, [ok_dir_id])
        print(f'Загрузка фотографий из альбома "{key}"')
        for photo in tqdm.tqdm(value):
            url = photo[1]
            name = photo[0]
            g.upload_from_internet(url=url, name=name, parents=[g.get_id(key)])

    with open('log.json', 'w') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    g.upload_file('log.json', 'log.json', [ok_dir_id])
