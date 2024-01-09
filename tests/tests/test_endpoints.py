import requests
from fastapi import HTTPException
import json

from cfg_tests import SESSION_COOKIE_FIELD, ADDRESS
from tools import register, login, add_offers, get_offers


def test_register_ok():
    register_response = register('test14', 'test3')
    assert json.loads(register_response.text) == 'user test14 created'

def test_register_login_used():
    register_response = register('test4', 'test3')
    assert json.loads(register_response.text).get('detail') == 'Username already exists'

def test_login_ok():
    login_response, cookie = login('test12', 'test3')
    assert json.loads(login_response.text) == 'created session for test12'

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
