from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    """Modèle d'un produit"""
    product_id: str
    name: str
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

class ProductResponse(BaseModel):
    """Réponse API pour un produit"""
    product_id: str
    name: str
    category: Optional[str] = None
    price: Optional[float] = None