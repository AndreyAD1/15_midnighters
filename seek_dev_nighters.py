import requests


def get_api_pages(number_of_api_pages):
    attempts_link = 'http://devman.org/api/challenges/solution_attempts'
    for page_number in range(number_of_api_pages):
        page_for_request = page_number + 1
        request_parameters = {'page': page_for_request}
        api_page = requests.get(attempts_link, request_parameters)
        yield api_page


def get_all_attempts():
    all_attempts = []
    number_of_pages = 3
    for api_page in get_api_pages(number_of_pages):
        attempt_list = api_page.json()['records']
        all_attempts.extend(attempt_list)
    return all_attempts


def get_midnighters():
    pass


if __name__ == '__main__':
    attempts_list = get_all_attempts()
    print(attempts_list)
