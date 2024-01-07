import logging


def index_document(es, index_name, doc, doc_id):
    return es.index(index=index_name, id=doc_id, body=doc)


def delete_indexed_document(es, index_name, doc_id):
    return es.delete(index=index_name, id=doc_id)


def create_index(es, index_name, logger: logging.Logger):
    mapping = {
        "properties": {
            "location": {
                "type": "geo_point"
            },
        }
    }
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={"mappings": mapping})
        logger.info(f"Index '{index_name}' created.")
    else:
        logger.info(f"Index '{index_name}' already exists.")
