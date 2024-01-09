from fastapi.testclient import TestClient

from ..main import app
from ..models.dishes import get_tags_map_low

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_read_tags():
    assert get_tags_map_low() == {
                                    0: "vegetarian",
                                    1: "gluten free",
                                    2: "sugar free",
                                    3: "should be warm",
                                    4: "spicy"
                                }
