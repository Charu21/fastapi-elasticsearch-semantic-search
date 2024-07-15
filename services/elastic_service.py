from injector import inject
from services.csv_loader import CSVLoader
from services.elastic_search_index_service import ElasticSearchIndex
from services.model_embedding_service import ModelEmbeddingService
from model.product import ProductResponse, PaginatedResponse
from typing import List, Optional
import logging


log = logging.getLogger(__name__)

class ElasticService:
    @inject
    def __init__(self, csv_loader: CSVLoader, elastic_index: ElasticSearchIndex, embedding_service: ModelEmbeddingService):
        self.csv_loader = csv_loader
        self.elastic_index = elastic_index
        self.embedding_service = embedding_service

    def index_all_products(self):
        """Index all of the products in the csv file.

            Returns:
            indexed_products (list): list of the indexed products
        """
        indexed_products = []
        product_list = self.csv_loader.load()
        if len(product_list) > 0:
            for product in product_list:
                try:
                    if isinstance(product, dict) and "Description" in product:
                        product["ProductID"] = int(product.get("ProductID", 0))
                        product["Price (INR)"] = int(product.get("Price (INR)", 0))
                        product["NumImages"] = int(product.get("NumImages", 0))
                        product["DescriptionVector"] = self.embedding_service.encode(product["Description"])
                        log.info(f"Indexing product: {product}")
                        self.elastic_index.add_document(product, product.get('ProductID'))
                        indexed_products.append((product.get('ProductID', 'N/A'), product.get('ProductName', 'N/A')))
                    else:
                        log.error(f"Invalid product format: {product}")
                except Exception as e:
                    log.error(f"Error indexing product: {e}")
        return indexed_products

    def add_document(self, text):
        self.elastic_index.add_document()
        embedding = self.embedding_service.encode(text).tolist()
        doc = {
            'text': text,
            'embedding': embedding
        }
        return self.client.index(index=self.index_name, body=doc)

    def search_data(self, query: str):
        """Search product in ElasticSearch based on input query semantically.

            Parameters:
            query (str): Query String

            Returns:
            A dict of products with the following products:
            doc_id (str): unique ID of the product document
            product_record (dict): Product document found in ElasticSearch
        """
        response = []
        if query is not None:
            encoded_query = self.embedding_service.encode(query)
            res = self.elastic_index.search(encoded_query)

            for product in res:
                source = product['_source']
                product_response = ProductResponse(
                    ProductID=source['ProductID'],
                    ProductName=source['ProductName'],
                    ProductBrand=source['ProductBrand'],
                    Price=source['Price (INR)'],
                    Description=source['Description']
                )
                response.append(product_response)
            
        return response
    
    def get_all_documents(self, cursor: Optional[str] = None, size: int = 10) -> PaginatedResponse:
        search_body = {
            "size": size,
            "sort": [
                {"ProductID": "asc"}
            ]
        }

        if cursor:
            search_body["search_after"] = [cursor]

        search_body["query"] = {
            "match_all": {}
        }

        res = self.elastic_index.client.search(index=self.elastic_index.index_name, body=search_body)
        products = []
        next_cursor = None

        if res is not None and res['hits']['hits']:
            for product in res['hits']['hits']:
                source = product['_source']
                product_response = ProductResponse(
                    ProductID=source['ProductID'],
                    ProductName=source['ProductName'],
                    ProductBrand=source['ProductBrand'],
                    Price=source['Price (INR)'],
                    Description=source['Description']
                )
                products.append(product_response)
            
            next_cursor = res['hits']['hits'][-1]['sort'][0]  # Use the last product's sort value as the next cursor
        
        return PaginatedResponse(products=products, next_cursor=next_cursor)

    def get_product_by_id(self, product_id: int) -> Optional[ProductResponse]:
        try:
            res = self.elastic_index.client.get(index=self.elastic_index.index_name, id=product_id)
            source = res['_source']
            product_response = ProductResponse(
                ProductID=source['ProductID'],
                ProductName=source['ProductName'],
                ProductBrand=source['ProductBrand'],
                Price=source['Price (INR)'],
                Description=source['Description']
            )
            return product_response
        except Exception as e:
            log.error(f"Error retrieving product with ID {product_id}: {e}")
            return None
        
    def start_indexing(self):
        log.info("Waiting for the model to be loaded...")
        # Needed only first time to load the indexes then can be commented.
        # self.embedding_service.model_loaded.wait()  # Wait for the model to be loaded
        log.info("Starting indexing process...")
        # self.index_all_products()
        log.info("Indexing process completed.")