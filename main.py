import os
import time

import requests

from dotenv import load_dotenv
import telegram


def get_last_timestamp(dvmn_api_token):
    dvmn_api_url = 'https://dvmn.org/api/user_reviews/'
    headers = {'Authorization': dvmn_api_token}
    response = requests.get(dvmn_api_url, headers=headers)
    response.raise_for_status()
    return response.json()['results'][0]['timestamp']


def get_dvmn_api(dvmn_api_token, timestamp):
    dvmn_api_url_long_polling = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': dvmn_api_token}
    payload = {'timestamp': timestamp}
    response = requests.get(dvmn_api_url_long_polling, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    dvmn_api_token = os.getenv('DVMN_API_TOKEN')
    bot = telegram.Bot(token=os.getenv('TG_API_TOKEN'))
    chat_id = os.getenv('TG_CHAT_ID')
    timestamp = get_last_timestamp(dvmn_api_token)
    while True:
        try:
            response = get_dvmn_api(dvmn_api_token, timestamp)
            if response['status'] == 'found':
                timestamp = response['last_attempt_timestamp']
                lesson_title = response['new_attempts'][0]['lesson_title']
                lesson_url = response['new_attempts'][0]['lesson_url']
                if response['new_attempts'][0]['is_negative']:
                    text = f'Ваша работа "{lesson_title}" проверена. К сожалению, в работе есть ошибки! ' \
                           f'Вот ссылка: {lesson_url}'
                else:
                    text = f'Ваша работа "{lesson_title}" проверена. ' \
                           f'Все хорошо, можно приступать к следующему уроку! ' \
                           f'Вот ссылка: {lesson_url}'
                bot.send_message(text=text, chat_id=chat_id)
            else:
                print('timeout')
                timestamp = response['timestamp_to_request']
        except requests.exceptions.Timeout:
            print('timeout')
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            time.sleep(5)


if __name__ == '__main__':
    main()
