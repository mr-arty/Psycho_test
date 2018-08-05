import requests
import settings
import json
from questions import *
from time import sleep

global URL
URL = 'https://api.telegram.org/bot' + settings.API_token
global last_update_id
last_update_id = 0

b = []  #Объявляем пустой массив

def send_req():
    # payload = {'key':settings.API_token}

    r = requests.get(URL + '/getMe')  #get-запрос
    r = r.json()
    print(r)

def get_updates():
    r = requests.get(URL + '/getupdates')
    r = r.json()
    return r

def get_message():
    data = get_updates()

    last_object = data['result'][-1]
    cur_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != cur_update_id:
        last_update_id = cur_update_id
        chat_id = last_object['message']['chat']['id']
        text = last_object['message']['text']
        message = {'chat_id': chat_id,
                   'text': text,
                   'update_id': cur_update_id}
        return message
    return None


def send_message(chat_id, text = 'Wait, please...'):
    requests.get(URL + '/sendmessage?chat_id={}&text={}'.format(chat_id, text))

def test(chat_id):
    send_message(chat_id, 'Привет! Я предлагаю тебе пройти очень простой психологический тест.')
    send_message(chat_id, 'В нем всего несколько простых вопросов. Для ответа введи или - на клавиатуре.')
    i = 0
    points = 0
    while i < 12:
        send_message(chat_id, a[i])
        sleep(10)

        if get_message() is not None:
            m = get_message()     #TypeError: 'NoneType' object is not subscriptable
            ans = m['text']
        else:
            ans = 0
            continue

        if ans == '+':
            points += 1
        elif ans == '-':
            i += 1
            continue
        else:
            send_message(chat_id, 'Пожалуйста, введи + или -')
            continue
        i += 1
    if points <= 4:
        send_message(chat_id, 'С тобой все хорошо! Фрустрация отсутствует.')
        b.append('a')
    elif points <= 9:
        send_message(chat_id, 'У тебя есть тенденция к фрустрации. Тебе нужно немного расслабиться!')
        b.append('b')
    else:
        send_message(chat_id, 'Внимание! У тебя сильная фрустрация. Обратись к психологу!')
        b.append('c')
    send_message(chat_id,'Тест окончен. Спасибо!')
    return True

def main():
    sleep(10)
    m = get_message()
    chat_id_c = m['chat_id']
    text = m['text']

    if text == '/start':
        while True:
            test(chat_id_c)
            send_message(chat_id_c, 'Хочешь сыграть еще раз?')
            sleep(10)
            if text == '/finish' or text == 'нет':
                break
            elif text == 'да':
                continue
if __name__ == '__main__':
    main()