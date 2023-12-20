from elasticsearch import Elasticsearch

from es_tools import get_by_fulltext
from config_copy import OFFER_INDEX


if __name__ == '__main__':

    fields = ["description"]
    query = "hdyż"

    es = Elasticsearch("http://localhost:9200")

    result = get_by_fulltext(es, OFFER_INDEX, fields, query)
    print(result)
