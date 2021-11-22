import os
import textwrap
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


def get_lesson_check(dvmn_api_token, timestamp):
    dvmn_api_url_long_polling = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': dvmn_api_token}
    payload = {'timestamp': timestamp}
    response = requests.get(dvmn_api_url_long_polling, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    dvmn_api_token = os.environ['DVMN_API_TOKEN']
    bot = telegram.Bot(token=os.environ['TG_API_TOKEN'])
    chat_id = os.environ['TG_CHAT_ID']
    timestamp = get_last_timestamp(dvmn_api_token)
    while True:
        try:
            response = get_lesson_check(dvmn_api_token, timestamp)
            if response['status'] == 'found':
                timestamp = response['last_attempt_timestamp']
                for attempt in response['new_attempts']:
                    lesson_title = attempt['lesson_title']
                    lesson_url = attempt['lesson_url']
                    if attempt['is_negative']:
                        text = f'''\
                        Ваша работа "{lesson_title}" проверена. К сожалению, в работе есть ошибки!
                        Вот ссылка: {lesson_url}
                        '''
                    else:
                        text = f'''\
                        Ваша работа "{lesson_title}" проверена.
                        Все хорошо, можно приступать к следующему уроку!
                        Вот ссылка: {lesson_url}'''
                    bot.send_message(text=textwrap.dedent(text), chat_id=chat_id)
            else:
                timestamp = response['timestamp_to_request']
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            time.sleep(5)


if __name__ == '__main__':
    main()
