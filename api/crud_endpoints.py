from fastapi import APIRouter, Depends, HTTPException
from services.elastic_service import ElasticService
from dependencies import get_elastic_service
from model.product import SearchQuery, ProductResponse, PaginatedResponse
from typing import List, Optional

import logging

router = APIRouter()

@router.post("/search_product", response_model=List[ProductResponse])
async def search_product(search_query: SearchQuery, elastic_service: ElasticService = Depends(get_elastic_service)):
    try:
        results = elastic_service.search_data(search_query.query)
        return results
    except Exception as e:
        logging.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_product/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, elastic_service: ElasticService = Depends(get_elastic_service)):
    try:
        product = elastic_service.get_product_by_id(product_id)
        if product:
            return product
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        logging.error(f"Error retrieving product: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get_all_products", response_model=PaginatedResponse)
async def get_all_products(cursor: Optional[str] = None, size: int = 10, elastic_service: ElasticService = Depends(get_elastic_service)):
    try:
        response = elastic_service.get_all_documents(cursor=cursor, size=size)
        return response
    except Exception as e:
        logging.error(f"Error retrieving documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))