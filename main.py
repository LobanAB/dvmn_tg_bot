import os
import time

import requests

from dotenv import load_dotenv
import telegram


def get_last_timestamp(dvmn_api_token):
    dvmn_api_url= 'https://dvmn.org/api/user_reviews/'
    headers = {
        'Authorization': dvmn_api_token
    }
    response = requests.get(dvmn_api_url, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    return response_json['results'][0]['timestamp']


def get_dvmn_api(dvmn_api_token, timestamp):
    # dvmn_api_url= 'https://dvmn.org/api/user_reviews/'
    dvmn_api_url_long_polling = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': dvmn_api_token
    }
    payload = {'timestamp': timestamp
               }
    response = requests.get(dvmn_api_url_long_polling, headers=headers, params=payload, timeout=5)
    response.raise_for_status()
    response_json = response.json()
    if response_json['status'] == 'found':
        print(response_json)
        return response_json['last_attempt_timestamp']
    else:
        print('timeout')
        return response_json['timestamp_to_request']


def main():
    load_dotenv()
    dvmn_api_token = os.getenv('DVMN_API_TOKEN')
    timestamp = get_last_timestamp(dvmn_api_token)
    bot = telegram.Bot(token=os.getenv('TG_API_TOKEN'))
    print(bot.get_me())
    updates = bot.get_updates()
    print(updates[0])
    bot.send_message(text='Привет', chat_id=465065578)
    '''
    while True:
        try:
            timestamp = get_dvmn_api(dvmn_api_token, timestamp)
        except requests.exceptions.Timeout:
            print('timeout')
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            time.sleep(5)
    '''

if __name__ == '__main__':
    main()
