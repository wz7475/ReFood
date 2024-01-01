import requests

from cfg_tests import SESSION_COOKIE_FIELD, ADDRESS
from tools import register, login


# ADDRESS = 'http://api:80'
def test_dummy_root():
    register_response = register()
    assert register_response.status_code == 200
    login_response, cookie = login()
    assert login_response.status_code == 200
    response = requests.get(f"{ADDRESS}/", cookies={SESSION_COOKIE_FIELD: cookie})
    assert response.status_code == 200
    assert response.json() == 'ReFood'

if __name__ == '__main__':
    test_dummy_root()