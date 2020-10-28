import Yauploader
import InstagrammAPI
import json
import tqdm


def run():

    inst_token = str(input('Введите токен доступа Инстаграма: '))

    inst_api = InstagrammAPI.InstagramAPI(inst_token)
    yauploader = Yauploader.YaUploader(str(input('Введите токен ЯндексДиска: ')))

    all_photos = inst_api.get_photos_info()
    log = inst_api.get_photos_log(all_photos)

    yauploader.mk_dir('instagram/')
    for photo in tqdm.tqdm(all_photos):
        path = 'instagram/'
        url = photo[1]
        name = f'{photo[0]}.jpg'
        yauploader.upload_from_internet(url, (path + name))

    with open('log.json', 'w') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    with open('log.json', "rb") as f:
        yauploader.upload(yauploader.get_upload_url('instagram/log.json'), f)
