import requests
import settings
import json
from time import sleep

global URL
URL = 'https://api.telegram.org/bot' + settings.API_token
global last_update_id
last_update_id = 0

a = []
a.append('1. Вы завидуете благополучию некоторых своих знакомых.')  # список вопросов
a.append('2. Вы недовольны отношениями в семье.')
a.append('3. Вы считаете, что достойны лучшей участи.')
a.append('4. Вы полагаете, что смогли бы достичь большего в личной жизни или в работе, если бы не обстоятельства.')
a.append('5. Вас огорчает то, что не осуществляются планы и не сбываются надежды.')
a.append('6. Вы часто срываете зло или досаду на ком-либо.')
a.append('7. Вас злит, что кому-то везет в жизни больше, чем вам.')
a.append('8. Вас огорчает, что вам не удается отдыхать или проводить досуг так, как того хочется.')
a.append('9. Ваше материальное положение таково, что угнетает вас.')
a.append('10. Вы считаете, что жизнь проходит мимо вас (проходит зря).')
a.append('11. Кто-то или что-то постоянно унижает вас.')
a.append('12. Нерешенные бытовые проблемы выводят вас из равновесия.')


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
#get_message()

def send_message(chat_id, text = 'Wait, please...'):
    requests.get(URL + '/sendmessage?chat_id={}&text={}'.format(chat_id, text))

def test(chat_id):
    send_message(chat_id, 'Привет! Я предлагаю тебе пройти очень простой психологический тест.')
    send_message(chat_id, 'В нем всего несколько простых вопросов. Для ответа введи + или - на клавиатуре.')
    i = 0
    points = 0
    while i < 12:
        send_message(chat_id, a[i])
        sleep(15)

        ans = get_message()['text']


        if ans == None:
            continue
        elif ans == '+':
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
    elif points <= 9:
        send_message(chat_id, 'У тебя есть тенденция к фрустрации. Тебе нужно немного расслабиться!')
    else:
        send_message(chat_id, 'Внимание! У тебя сильная фрустрация. Обратись к психологу!')
    send_message(chat_id,'Тест окончен. Спасибо!')

def main():
    sleep(10)
    m = get_message()
    chat_id_c = m['chat_id']
    text = m['text']

    if text == '/start':
        test(chat_id_c)
        #send_message(chat_id, 'I\'m doin fine, g')

if __name__ == '__main__':
    main()