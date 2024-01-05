from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Refood multiple files"}


def test_read_tags():
    response = client.get("/get_tags_map")
    assert response.status_code == 200
    assert response.json() == {
                                "0": "vege",
                                "1": "glutenFree",
                                "2": "sugarFree",
                                "3": "shouldBeWarm",
                                "4": "spicy"
                                }