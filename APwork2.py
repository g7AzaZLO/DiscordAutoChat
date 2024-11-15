from deep_translator import GoogleTranslator
from random import choice, sample
from string import punctuation
import requests as req
import schedule
from generator import generatetext
from time import sleep
from datetime import datetime
from websocket import create_connection

print("""
╔═══╗╔╗─╔╗╔════╗╔═══╗╔═══╗╔╗─╔╗╔═══╗╔════╗
║╔═╗║║║─║║║╔╗╔╗║║╔═╗║║╔═╗║║║─║║║╔═╗║║╔╗╔╗║ 
║║─║║║║─║║╚╝║║╚╝║║─║║║║─╚╝║╚═╝║║║─║║╚╝║║╚╝
║╚═╝║║║─║║──║║──║║─║║║║─╔╗║╔═╗║║╚═╝║──║║──
║╔═╗║║╚═╝║──║║──║╚═╝║║╚═╝║║║─║║║╔═╗║──║║── By 
╚╝─╚╝╚═══╝──╚╝──╚═══╝╚═══╝╚╝─╚╝╚╝─╚╝──╚╝──    AzaZlo""")

# Ввод параметров
token = input("[X] Вставьте токен юзера, от которого будет производиться отправка\n>> ")
channels = {}
while True:
    channel_id = input("[X] Вставьте ID канала для отправки сообщений (или нажмите Enter для завершения):\n>> ")
    if not channel_id:
        break
    language = input(f"[X] Укажите язык перевода для канала {channel_id} (например, 'ru', 'en', 'fr'):\n>> ")
    channels[channel_id] = language

question = input('[X] Введите "1" для задержки в секундах, "2" в минутах, "3" в часах, "4" в днях\n>> ')
timer = input("[X] Введите через какое количество секунд/минут/часов/дней будет отправляться сообщение\n>> ")

# Функция для отправки сообщений
def send_message(token, channels):
    for channel_id, language in channels.items():
        # Генерация нового текста
        original_message = generatetext()
        print(f"[X] Сгенерированный текст (англ.) для канала {channel_id}: {original_message}")

        # Перевод на указанный язык
        try:
            translated_message = GoogleTranslator(source='auto', target=language).translate(original_message)
            print(f"[X] Переведённый текст для канала {channel_id} ({language}): {translated_message}")
        except Exception as e:
            print(f"[X] Ошибка при переводе для канала {channel_id}: {e}")
            translated_message = "Ошибка перевода."

        # Отправка сообщения
        s = req.Session()
        s.headers.update({'authorization': token, 'Content-Type': 'application/json'})
        payload = {"content": translated_message, "tts": False}

        try:
            # WebSocket соединение
            ws = create_connection("wss://gateway.discord.gg/")
            data = '''
            {
                "op": 2,
                "d": {
                    "token": "%s",
                    "properties": {
                        "$os": "linux",
                        "$browser": "ubuntu",
                        "$device": "ubuntu"
                    }
                }
            }
            ''' % token
            ws.send(data)
            ws.close()

            # Отправка сообщения
            response = s.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json=payload)
            response.raise_for_status()
            current_datetime = datetime.now()
            print(f"[X] {current_datetime} | Сообщение успешно отправлено в канал {channel_id}: {translated_message}")
        except Exception as e:
            print(f"[X] Ошибка при отправке сообщения в канал {channel_id}: {e}")


# Планировщик
def schedule_messages():
    send_message(token, channels)

if question == "1":
    schedule.every(int(timer)).seconds.do(schedule_messages)
elif question == "2":
    schedule.every(int(timer)).minutes.do(schedule_messages)
elif question == "3":
    schedule.every(int(timer)).hours.do(schedule_messages)
elif question == "4":
    schedule.every(int(timer)).days.do(schedule_messages)
else:
    print("[X] Указано неверное значение задержки")
    exit()

print("[X] Автоотправка сообщений успешно запущена, приятного пользования.")
while True:
    schedule.run_pending()
    sleep(1)
