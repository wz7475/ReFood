import uuid


def get_uuid_string():
    return str(uuid.uuid4())


# ADDRESS = 'http://127.0.0.1:8080'
ADDRESS = 'http://maluch.mikr.us:40481'
LOGIN = get_uuid_string()
PASSWORD = get_uuid_string()
SESSION_COOKIE_FIELD = 'sessionId'
