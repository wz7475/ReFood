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


def geta_all_data(es, index_name):
    query = {"query": {"match_all": {}}}
    return es.search(index=index_name, body=query)
