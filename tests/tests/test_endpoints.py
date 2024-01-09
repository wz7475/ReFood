import requests
from fastapi import HTTPException
import json

from cfg_tests import SESSION_COOKIE_FIELD, ADDRESS
from tools import register, login, add_offers, get_my_offers, get_offer_by_id


def test_register_ok():
    register_response = register('test20', 'test3')
    assert json.loads(register_response.text) == 'user test20 created'

def test_register_login_used():
    register_response = register('test20', 'test3')
    assert json.loads(register_response.text)['detail'] == 'Username already exists'

def test_login_ok():
    login_response, cookie = login('test20', 'test3')
    assert json.loads(login_response.text) == 'created session for test20'

def test_login_bad_login():
    try:
        login_response, cookie = login('bad_login', 'test3555')
    except HTTPException as e:
        assert HTTPException.status_code == 401
        assert HTTPException.detail == 'User does not exist'

def test_login_bad_password():
    try:
        login_response, cookie = login('test4', 'test3555')
    except HTTPException as e:
        assert HTTPException.status_code == 401
        assert HTTPException.detail == "Incorrect password"

def test_e2e_add_offer():
    test_login = 'test29'
    register_response = register(test_login, 'test3')
    assert json.loads(register_response.text) == f'user {test_login} created'
    login_response, cookie = login(test_login, 'test3')
    assert json.loads(login_response.text) == f'created session for {test_login}'
    response = get_my_offers(cookie)
    assert len(response.json()) == 0
    response_offer_id = add_offers(cookie)
    assert isinstance(response_offer_id.json(), int)
    response_get = get_my_offers(cookie)
    assert len(response_get.json()) > 0
    response = get_offer_by_id(cookie, response_offer_id.json())
    assert response.json()['dish_description'] == "to nmoże są banany"