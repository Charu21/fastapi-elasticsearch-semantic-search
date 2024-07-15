from elasticsearch import Elasticsearch
from config.elastic_mapper import product_mapping

def initialize_elasticsearch():
    es = Elasticsearch()
    if not es.indices.exists(index="products"):
        es.indices.create(index="products", body=product_mapping)
    return es

if __name__ == "__main__":
    es = initialize_elasticsearch()
    print("Elasticsearch initialized with the given mappings.")
