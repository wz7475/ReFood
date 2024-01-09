curl -X POST -H "Content-Type: application/json" -d \
'{"name": "w1", "surname": "your_surname", "login": "w1", "password": "1234", "phone_nr": "123456789"}' \
http://localhost:8080/register

curl -X POST -H "Content-Type: application/json" -d \
'{"login": "w1", "password": "1234"}' http://localhost:8080/login --cookie-jar cookie.txt && cat cookie.txt && rm cookie.txt

curl -X POST -H "Content-Type: application/json" -d \
'{"latitude": 50.06143, "longitude": 19.93658, "dish_name": "Example3 Dish", "how_many_days_before_expiration": 2, "description": "This is an example dish", "price": 1000, "tags": []}' \
http://localhost:8080/offers --cookie "cookie.txt"

curl http://localhost:8080/test-es-query/example --cookie "cookie.txt"

curl -X DELETE http://localhost:8080/offers/1 --cookie "cookie.txt"

curl --location 'http://localhost:8080/offers' \
--cookie "cookie.txt" \
--header 'Content-Type: application/json' \
--data '{
    "latitude": 1,
    "longitude": 1,
    "dish_name": "chleb",
    "description": "burak pyszny",
    "price": 1122,
    "how_many_days_before_expiration": 1,
    "tags": [0, 2]
}'


curl --location 'http://localhost:8080/offers/filter' \
--cookie "cookie.txt" \
--header 'Content-Type: application/json' \
--data '{
    "pattern": "burak",
    "tags": [0,1,2],
    "distance": -1,
    "lat": 51.4171713,
    "lon": 21.9720582
}'

# działa bez tagów
 curl -X GET "http://elasticsearch:9200/offers/_search" -H "Content-Type: application/json" -d'
        {
    "query": {
        "bool": {
            "must": [
                {
                    "multi_match": {
                        "query": "burak",
                        "fields": ["description", "dish_name"]
                    }
                }
            ]
        }
    }
}
'

# tagi
 curl -X GET "http://elasticsearch:9200/offers/_search" -H "Content-Type: application/json" -d'
        {
    "query": {
        "bool": {
            "must": [
                {
                    "multi_match": {
                        "query": "burak",
                        "fields": ["description", "dish_name"]
                    }
                },
                {
                        "terms": {"tags": [0]}
                }
            ]
        }
    }
}
'


curl -X GET "http://elasticsearch:9200/offers/_search" -H "Conten
t-Type: application/json"curl -X GET "http://elasticsearch:9200/offers/_search" -H "Content-Type: application/json" -d'
{
  "query": {
    "match_all": {}
  }
}' | grep burak

{"took":1,"timed_out":false,"_shards":{"total":1,"successful":1,"skipped":0,"failed":0},"hits":{"total":{"value":4,"relation":"eq"},"max_score":1.0,"hits":[{"_index":"offers","_type":"_doc","_id":"3","_score":1.0,"_source":{"dish_name":"chleb","description":"burak pyszny","tags":[0,2],"location":{"lat":1.0,"lon":1.0}}},{"_index":"offers","_type":"_doc","_id":"0","_score":1.0,"_source":{"dish_name":"kolejna chleb","description":"pyszny chleb","tags":[0,2],"location":{"lat":1.0,"lon":1.0}}},{"_index":"offers","_type":"_doc","_id":"1","_score":1.0,"_source":{"dish_name":"kolejna chleb","description":"pyszny chleb","tags":[0,2],"location":{"lat":1.0,"lon":1.0}}},{"_index":"offers","_type":"_doc","_id":"2","_score":1.0,"_source":{"dish_name":"chleb","description":"chleb pyszny","tags":[0,2],"location":{"lat":1.0,"lon":1.0}}}]}}
