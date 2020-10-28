import vk_to_yandex
import vk_to_google
import inst_to_google
import inst_to_YA
# import ok_to_yandex
# import ok_to_google

comands = {
    'vy': vk_to_yandex,
    'vg': vk_to_google,
    'iy': inst_to_YA,
    'ig': inst_to_google,
    # 'oy': ok_to_yandex,
    # 'og': ok_to_google
}

photo_serv = ['v', 'i', 'o']
cloud_serv = ['y', 'g']


def run():
    answer = str()
    comand = str()
    print('Добрый день!')
    while answer not in photo_serv:
        answer = input('Выберите социальную сеть\nv - Вконтакте\ni - Instagram\no - Одноклассники\n')
    comand += answer
    while answer not in cloud_serv:
        answer = input('Выберите облачный сервис\ny - ЯндексДиск\ng - GoogleDrive\n')
    comand += answer
    return comands[comand].run()

run()