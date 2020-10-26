import Yauploader
import Vkapi
import json
import tqdm


def run():

    apivk = Vkapi.ApiVK(str(input('Введите ID страницы Вконтакте: ')))
    yauploader = Yauploader.YaUploader(str(input('Введите токен ЯндексДиска: ')))

    all_photos = apivk.get_photos_info(apivk.get_albums())
    log = apivk.get_photos_log(all_photos)

    yauploader.mk_dir('vk/')
    for key, value in all_photos.items():
        path = 'vk/' + key + '/'
        print(f'Загрузка фотографий из альбома "{key}"')
        for photo in tqdm.tqdm(value):
            url = photo[1]
            name = photo[0]
            yauploader.mk_dir(path)
            yauploader.upload_from_internet(url, (path + name))

    with open('log.json', 'w') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    with open('log.json', "rb") as f:
        yauploader.upload(yauploader.get_upload_url('vk/log.json'), f)
