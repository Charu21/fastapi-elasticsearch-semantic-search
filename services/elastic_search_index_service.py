from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import logging

log = logging.getLogger(__name__)

class ElasticSearchFactory:
    def __init__(self, host: str, port: int):
        self.client = Elasticsearch([{'host': host, 'port': port}])

class ElasticSearchIndex:
    def __init__(self, factory: ElasticSearchFactory, index_name: str, product_mapping: dict):
        self.client = factory.client
        self.index_name = index_name
        self.product_mapping = product_mapping
        self.create_index()

    def create_index(self):
        if not self.client.indices.exists(index=self.index_name):
            index_settings = {
                    "settings": self.product_mapping.get("settings", {}),
                    "mappings": self.product_mapping.get("mappings", {})
                    }
            self.client.indices.create(index=self.index_name, body=index_settings)

    def add_document(self, document, document_id=None):
        return self.client.index(index=self.index_name, id=document_id, body=document)

    def search(self, query_embedding):
        # query_embedding = query.tolist()
        search_body = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'DescriptionVector') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
        }
        try:
            res = self.client.search(index=self.index_name, body=search_body)
            return res['hits']['hits']
        except Exception as e:
            log.error(f"Error searching documents: {e}")
            raise e

    def index_exists(self, index_name: str) -> bool:
        name_of_curr_index = index_name if index_name else self.index_name
        return self.client.indices.exists(index=name_of_curr_index)

    def document_exists(self, index_name: str, doc_id: str) -> bool:
        name_of_curr_index = index_name if index_name else self.index_name
        try:
            return self.client.exists(index=name_of_curr_index, id=doc_id)
        except NotFoundError:
            return False
    
    def count_documents(self, index_name: str) -> int:
        name_of_curr_index = index_name if index_name else self.index_name
        response = self.client.count(index=name_of_curr_index)
        return response['count']
