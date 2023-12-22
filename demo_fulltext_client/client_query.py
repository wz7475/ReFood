import sys

from elasticsearch import Elasticsearch

from es_tools import get_by_fulltext
from config import OFFER_INDEX

if __name__ == '__main__':
    fields = ["description"]
    query = sys.argv[1]

    es = Elasticsearch("http://localhost:9200")

    result = get_by_fulltext(es, OFFER_INDEX, fields, query)
    print(result)
