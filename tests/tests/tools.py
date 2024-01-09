import random

import requests

from cfg_tests import ADDRESS, get_uuid_string, LOGIN, PASSWORD, SESSION_COOKIE_FIELD


def get_random_phone_number()->str:
    return str(random.randint(100000000, 999999999))


def register():
    response = requests.post(ADDRESS + '/register', json={
        'name': get_uuid_string(),
        'surname': get_uuid_string(),
        'login': LOGIN,
        'password': PASSWORD,
        'phone_nr': get_random_phone_number()
    })
    return response

def login():
    response = requests.post(ADDRESS + '/login', json={
        'login': LOGIN,
        'password': PASSWORD
    })
    session_cookie = response.cookies.get(SESSION_COOKIE_FIELD)
    return response, session_cookie
