import vk_to_google
import vk_to_yandex

answer = input('Добрый день! Выберите какой облачный сервис вы используете (g, ya, q - выход): ')
if answer == 'g':
    vk_to_google.run()
elif answer == 'ya':
    vk_to_yandex.run()
elif answer == 'q':
    print('До свидания!')
else:
    print('Ошибка ввода! Перезапустите программу!')