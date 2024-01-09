import requests
from fastapi import HTTPException
import json
import time

from cfg_tests import SESSION_COOKIE_FIELD, ADDRESS
from tools import register, login, add_offers, get_my_offers, get_offer_by_id, delete_offer_by_id

def get_random_login():
    return str(time.time_ns())

def test_register_ok_and_register_login_used():
    test_login = get_random_login()
    register_response = register(test_login, 'haslo')
    assert register_response.json() == f'user {test_login} created'
    register_response = register(test_login, 'test3')
    assert register_response.json()['detail'] == 'Username already exists'

def test_login_ok():
    test_login = get_random_login()
    register_response = register(test_login, 'haslo')
    assert register_response.json() == f'user {test_login} created'
    login_response, cookie = login(test_login, 'haslo')
    assert json.loads(login_response.text) == f'created session for {test_login}'

def test_login_bad_login():
    try:
        login_response, cookie = login(get_random_login(), 'test3555')
    except HTTPException as e:
        assert HTTPException.status_code == 401
        assert HTTPException.detail == 'User does not exist'

def test_login_bad_password():
    test_login = get_random_login()
    register_response = register(test_login, 'haslo')
    assert register_response.json() == f'user {test_login} created'
    
    try:
        login_response, cookie = login(test_login, 'zle_haslo')
    except HTTPException as e:
        assert HTTPException.status_code == 401
        assert HTTPException.detail == "Incorrect password"

def test_e2e_add_offer():
    test_login = get_random_login()
    register_response = register(test_login, 'haslo')
    assert json.loads(register_response.text) == f'user {test_login} created'
    login_response, cookie = login(test_login, 'haslo')
    assert json.loads(login_response.text) == f'created session for {test_login}'
    response = get_my_offers(cookie)
    assert len(response.json()) == 0
    response_offer_id = add_offers(cookie)
    assert isinstance(response_offer_id.json(), int)
    response_get = get_my_offers(cookie)
    assert len(response_get.json()) > 0
    response = get_offer_by_id(cookie, response_offer_id.json())
    assert response.json()[0]['dish_description'] == "to nmoże są banany"
    response_delete = delete_offer_by_id(cookie, response_offer_id.json())
    try:
        response_get_by_id = get_offer_by_id(cookie, response_offer_id.json())
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Offer not found"