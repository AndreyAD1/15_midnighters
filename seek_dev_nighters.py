import requests
import pytz
from datetime import datetime, time
from collections import defaultdict


def get_api_pages(page):
    attempts_link = 'http://devman.org/api/challenges/solution_attempts'
    request_parameters = {'page': page}
    api_page = requests.get(attempts_link, request_parameters)
    return api_page


def get_all_attempts():
    attempts = []
    page = 1
    while True:
        api_page = get_api_pages(page)
        if not api_page:
            return attempts
        page_attempts = api_page.json()['records']
        attempts.extend(page_attempts)
        page += 1


def get_local_time_of_attempts(attempts):
    local_time_of_attempts = defaultdict(list)
    for attempt in attempts:
        utc_date_of_attempt = datetime.utcfromtimestamp(attempt['timestamp'])
        user_timezone = pytz.timezone(attempt['timezone'])
        local_date = user_timezone.localize(utc_date_of_attempt)
        local_time = local_date.time()
        user = attempt['username']
        local_time_of_attempts[user].append(local_time)
    return local_time_of_attempts


def check_night_time_of_attempt(attempts_time_list):
    midnight = time()
    night_end = time(hour=6)
    for attempt_time in attempts_time_list:
        if midnight < attempt_time <= night_end:
            return True
    return


def get_midnighters(attempts_time_dict):
    midnighters_list = []
    for user in attempts_time_dict:
        attempts_time_list = attempts_time_dict[user]
        if check_night_time_of_attempt(attempts_time_list):
            midnighters_list.append(user)
    return midnighters_list


if __name__ == '__main__':
    all_attempts = get_all_attempts()
    local_time_of_users_attempts = get_local_time_of_attempts(all_attempts)
    midnighters = get_midnighters(local_time_of_users_attempts)
    print('Users who sent the assignment between 0:00 and 6:00:')
    for user in midnighters:
        print(user)
