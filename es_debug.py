from elasticsearch import Elasticsearch

def create_index(index_name):
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # Check if the index already exists
    if not es.indices.exists(index=index_name):
        # Create the index
        es.indices.create(index=index_name)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")

if __name__ == "__main__":
    # Specify the name of the index to be created
    index_name = "my_index"

    # Create the index
    create_index(index_name)
