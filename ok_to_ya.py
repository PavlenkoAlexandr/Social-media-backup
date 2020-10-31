import Yauploader
import okApi
import json
import tqdm


def run():

    application_key = input('Введите application key вашего приложения: ')
    token = input('Введите ваш токен доступа: ')
    secret_session_key = input('Введите ваш secret session key: ')

    okapi = okApi.OkApi(application_key, token, secret_session_key)
    yauploader = Yauploader.YaUploader(str(input('Введите токен ЯндексДиска: ')))

    all_photos = okapi.get_photos_info(okapi.get_albums())
    log = okapi.get_photos_log(all_photos)

    yauploader.mk_dir('ok/')
    for key, value in all_photos.items():
        path = 'ok/' + key + '/'
        print(f'Загрузка фотографий из альбома "{key}"')
        yauploader.mk_dir(path)
        for photo in tqdm.tqdm(value):
            url = photo[1]
            name = photo[0]
            yauploader.upload_from_internet(url, (path + name))

    with open('log.json', 'w') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    with open('log.json', "rb") as f:
        yauploader.upload(yauploader.get_upload_url('ok/log.json'), f)
