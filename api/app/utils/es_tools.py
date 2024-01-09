def get_by_fulltext(es, index_name, fields, search_text, list_of_tags):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": search_text,
                            "fields": fields
                        }
                    },
                    {
                        "terms": {"tags": list_of_tags}
                    }
                ]
            }
        }
    }
    return es.search(index=index_name, body=query)


def get_by_fulltext_distance(es, index_name, fields, search_text, list_of_tags, distance, lat, lon):
    distance = f"{distance}m"
    query = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": search_text,
                        "fields": fields
                    }
                },
                "filter": [
                    {
                        "geo_distance": {
                            "distance": distance,  # Adjust the distance as needed
                            "location": {
                                "lat": lat,  # Specify the latitude of the center point
                                "lon": lon  # Specify the longitude of the center point
                            }
                        }
                    },
                    {
                        "terms": {"tags": list_of_tags}
                    }
                ]
            }
        }
    }
    return es.search(index=index_name, body=query)


def get_all_data(es, index_name):
    query = {"query": {"match_all": {}}}
    return es.search(index=index_name, body=query)



