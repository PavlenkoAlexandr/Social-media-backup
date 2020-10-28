import InstagrammAPI
import GoogleDriveAPI
import tqdm
import json


def run():

    inst_token = str(input('Введите токен доступа Инстаграма: '))

    inst_api = InstagrammAPI.InstagramAPI(inst_token)
    g = GoogleDriveAPI.GoogleApi()

    all_photos = inst_api.get_photos_info()
    log = inst_api.get_photos_log(all_photos)

    g.make_dir('instagram')
    inst_dir_id = g.get_id('instagram')

    for photo in tqdm.tqdm(all_photos):
        url = photo[1]
        name = f'{photo[0]}.jpg'
        g.upload_from_internet(url=url, name=name, parents=[inst_dir_id])

    with open('log.json', 'w') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    g.upload_file('log.json', 'log.json', [inst_dir_id])
