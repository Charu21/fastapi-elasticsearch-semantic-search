from pydantic import BaseModel
from typing import List, Optional

class SearchQuery(BaseModel):
    query: str

class Product(BaseModel):
    ProductID: int
    ProductName: str
    ProductBrand: str
    Gender: str
    Price: int
    NumImages: int
    Description: str
    PrimaryColor: str
    DescriptionVector: List[float] = []

class ProductResponse(BaseModel):
    ProductID: int
    ProductName: str
    ProductBrand: str
    Price: int
    Description: str

class PaginatedResponse(BaseModel):
    products: List[ProductResponse]
    next_cursor: Optional[str]