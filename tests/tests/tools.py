import random

import requests
from uuid import uuid4
from cfg_tests import ADDRESS, get_uuid_string, LOGIN, PASSWORD, SESSION_COOKIE_FIELD

def get_random_phone_number()->str:
    return str(random.randint(100000000, 999999999))


def register(login, password):
    response = requests.post(ADDRESS + '/register', json={
        'name': get_uuid_string(),
        'surname': get_uuid_string(),
        'login': login,
        'password': password,
        'phone_nr': get_random_phone_number()
    })
    return response

def login(login, password):
    response = requests.post(ADDRESS + '/login', json={
        'login': login,
        'password': password
    })
    session_cookie = response.cookies.get(SESSION_COOKIE_FIELD)
    return response, session_cookie

def add_offers(cookie):
    response = requests.post(ADDRESS + '/offers', json={
        "latitude": 1,
        "longitude": 1,
        "dish_name": "kolejna taggi",
        "description": "to nmoże są banany",
        "price": 1122,
        "how_many_days_before_expiration": 1,
        "tags": [0, 2],
    }, cookies={SESSION_COOKIE_FIELD: cookie})
    return response

def get_my_offers(cookie):
    return requests.get(ADDRESS + '/my_offers', cookies={SESSION_COOKIE_FIELD: cookie})

def get_offer_by_id(cookie, offer_id):
    return requests.get(ADDRESS + f'/offers/{offer_id}', cookies={SESSION_COOKIE_FIELD: cookie})