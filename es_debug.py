from time import sleep

from elasticsearch import Elasticsearch
import warnings
warnings.filterwarnings("ignore")

def create_index(es, index_name):
    if not es.indices.exists(index=index_name):
        # Create the index
        es.indices.create(index=index_name)
        print(f"Index '{index_name}' created.")
    else:
        es.indices.delete(index=index_name)
        es.indices.create(index=index_name)
        print(f"Index '{index_name}' recreated.")


def index_offer(es, index_name, offer):
    es.index(index=index_name, id=offer["id"], body=offer)


def get_by_seller_id(es, index_name, seller_id):
    query = {
        "query": {
            "term": {
                "seller_id": seller_id
            }
        }
    }
    return es.search(index=index_name, body=query)

def get_by_fulltext(es, index_name, fields, search_text):
    query = {
        "query": {
            "multi_match": {
                "query": search_text,
                "fields": fields
            }
        }
    }
    return es.search(index=index_name, body=query)

def check_data(es, index_name):
    query = {"query": {"match_all": {}}}
    return es.search(index=index_name, body=query)

if __name__ == "__main__":
    es = Elasticsearch("http://localhost:9200")
    index_name = "offers"
    offer1 = {
        "id": 1,
        "dish_id": 1,
        "seller_id": 1,
        "address_id": 1,
        "creation_date": "2021-01-01",
        "description": "test1 hdyż",
    }
    offer2 = {
        "id": 2,
        "dish_id": 2,
        "seller_id": 2,
        "address_id": 2,
        "creation_date": "2022-01-02",
        "description": "test2 hdyż",
    }
    offer3 = {
        "id": 3,
        "dish_id": 3,
        "seller_id": 1,
        "address_id": 3,
        "creation_date": "2022-01-02",
        "description": "test3 hdyż",
    }
    # create_index(es, index_name)
    # sleep(1)
    index_offer(es, index_name, offer1)
    index_offer(es, index_name, offer2)
    index_offer(es, index_name, offer3)
    es.indices.refresh(index=index_name)
    # sleep(1)
    # response = get_by_seller_id(es, index_name, 2)
    response = get_by_fulltext(es, index_name, ["description"], "test1")
    # response = check_data(es, index_name)
    print(response)
    # for hit in response['hits']['hits']:
    #     print(hit["_source"])
    # print(get_by_fulltext(es, index_name, "2022"))
