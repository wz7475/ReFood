curl -X POST -H "Content-Type: application/json" -d \
'{"name": "w1", "surname": "your_surname", "login": "w1", "password": "1234", "phone_nr": "123456789"}' \
http://localhost:8080/register

curl -X POST -H "Content-Type: application/json" -d \
'{"login": "w1", "password": "1234"}' http://localhost:8080/login --cookie-jar cookie.txt && cat cookie.txt && rm cookie.txt

curl -X POST -H "Content-Type: application/json" -d \
'{"latitude": 50.06143, "longitude": 19.93658, "dish_name": "Example3 Dish", "how_many_days_before_expiration": 2, "description": "This is an example dish", "price": 1000, "tags": []}' \
http://localhost:8080/offers --cookie "cookie.txt"

curl http://localhost:8080/test-es-query/example --cookie "cookie.txt"

