# from fastapi import Depends
# from services.csv_loader import CSVLoader
# from services.elastic_search_index_service import ElasticSearchFactory, ElasticSearchIndex
# from services.model_embedding_service import ModelEmbeddingService
# from services.elastic_service import ElasticService
# from config.elastic_mapper import product_mapping
# import os

# def get_csv_loader() -> CSVLoader:
#     csv_path = os.getenv('CSV_PATH', os.getcwd() + '/resources/myntra_products.csv')
#     return CSVLoader(csv_path)

# def get_elastic_connection() -> ElasticSearchIndex:
#     host = os.getenv('ELASTIC_HOST', 'localhost')
#     port = int(os.getenv('ELASTIC_PORT', 9200))
#     index_name = os.getenv('ELASTIC_INDEX_NAME', 'semantic_search')
#     elastic_factory = ElasticSearchFactory(host, port)
#     return ElasticSearchIndex(elastic_factory, index_name, product_mapping)

# def get_embedding_service() -> ModelEmbeddingService:
#     model_name = os.getenv('BERT_MODEL', 'all-mpnet-base-v2')
#     return ModelEmbeddingService(model_name)

# def get_elastic_service(
#     csv_loader: CSVLoader = Depends(get_csv_loader),
#     elastic_index: ElasticSearchIndex = Depends(get_elastic_connection),
#     embedding_service: ModelEmbeddingService = Depends(get_embedding_service)
# ) -> ElasticService:
#     return ElasticService(csv_loader, elastic_index, embedding_service)

from fastapi import Depends
from services.csv_loader import CSVLoader
from services.elastic_search_index_service import ElasticSearchFactory, ElasticSearchIndex
from services.model_embedding_service import ModelEmbeddingService
from services.elastic_service import ElasticService
from config.elastic_mapper import product_mapping
import os
import threading

# Singleton for model embedding service
_model_service_instance = None
_model_service_lock = threading.Lock()

def get_csv_loader() -> CSVLoader:
    csv_path = os.getenv('CSV_PATH', os.getcwd() + '/resources/myntra_products.csv')
    return CSVLoader(csv_path)

def get_elastic_connection() -> ElasticSearchIndex:
    host = os.getenv('ELASTIC_HOST', 'localhost')
    port = int(os.getenv('ELASTIC_PORT', 9200))
    index_name = os.getenv('ELASTIC_INDEX_NAME', 'semantic_search')
    elastic_factory = ElasticSearchFactory(host, port)
    return ElasticSearchIndex(elastic_factory, index_name, product_mapping)

def get_embedding_service() -> ModelEmbeddingService:
    global _model_service_instance
    with _model_service_lock:
        if _model_service_instance is None:
            model_name = os.getenv('BERT_MODEL', 'all-mpnet-base-v2')
            _model_service_instance = ModelEmbeddingService(model_name)
    return _model_service_instance

def get_elastic_service(
    csv_loader: CSVLoader = Depends(get_csv_loader),
    elastic_index: ElasticSearchIndex = Depends(get_elastic_connection),
    embedding_service: ModelEmbeddingService = Depends(get_embedding_service)
) -> ElasticService:
    return ElasticService(csv_loader, elastic_index, embedding_service)
