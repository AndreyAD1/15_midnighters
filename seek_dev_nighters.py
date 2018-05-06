import requests
import pytz
from datetime import datetime


def load_attempts():
    attempts_link = 'http://devman.org/api/challenges/solution_attempts'
    page = 1
    while True:
        request_parameters = {'page': page}
        api_page = requests.get(attempts_link, request_parameters)
        api_page_json = api_page.json()
        for attempt in api_page_json['records']:
            yield attempt
        page += 1
        if page > api_page_json['number_of_pages']:
            break


def get_midnighters(attempts):
    midnighters = []
    midnight_hour = 0
    morning_hour = 6
    for attempt in attempts:
        attempt_local_datetime = get_local_datetime_of_attempt(attempt)
        if midnight_hour <= attempt_local_datetime.hour < morning_hour:
            attempt_user = attempt['username']
            if attempt_user not in midnighters:
                midnighters.append(attempt_user)
    return midnighters


def get_local_datetime_of_attempt(attempt_info):
    utc_datetime_of_attempt = datetime.utcfromtimestamp(attempt_info['timestamp'])
    user_timezone = pytz.timezone(attempt_info['timezone'])
    local_datetime_of_attempt = user_timezone.localize(utc_datetime_of_attempt)
    return local_datetime_of_attempt


if __name__ == '__main__':
    attempts_generator = load_attempts()
    midnighters_list = get_midnighters(attempts_generator)
    print('The users who has ever sent an assignment between 0:00 and 6:00:')
    for user in midnighters_list:
        print(user)
