import Vkapi
import GoogleDriveAPI
import tqdm
import json


def run():

    vk_id = str(input('Введите ID или User_name страницы Вконтакте: '))
    vk_token = str(input('Введите токен доступа ВК: '))

    apivk = Vkapi.ApiVK(vk_id, vk_token)
    apivk.user_id = apivk.get_userid(vk_id)
    g = GoogleDriveAPI.GoogleApi()

    all_photos = apivk.get_photos_info(apivk.get_albums())
    log = apivk.get_photos_log(all_photos)

    g.make_dir('vk')
    vk_dir_id = g.get_id('vk')

    for key, value in all_photos.items():
        g.make_dir(key, [vk_dir_id])
        print(f'Загрузка фотографий из альбома "{key}"')
        for photo in tqdm.tqdm(value):
            url = photo[1]
            name = photo[0]
            g.upload_from_internet(url=url, name=name, parents=[g.get_id(key)])

    with open('log.json', 'w') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    g.upload_file('log.json', 'log.json', [vk_dir_id])
