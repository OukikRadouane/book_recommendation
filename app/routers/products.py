from fastapi import APIRouter, HTTPException, Query
from app.services.mongodb_service import MongoDBService
from app.models.product import ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Récupère un produit par son ID"""
    product = await MongoDBService.get_product(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    
    return ProductResponse(
        product_id=product["product_id"],
        name=product.get("title", "Unknown"),
        category=product.get("category"),
        price=product.get("price")
    )

@router.get("/")
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: str = Query(None, description="Filtrer par catégorie")
):
    """Récupère la liste des produits (paginée, filtrable par catégorie)"""
    
    if category:
        products = await MongoDBService.get_products_by_category(category, limit)
    else:
        products = await MongoDBService.get_all_products(skip, limit)
    formatted_products = []
    for p in products:
        formatted_products.append({
            "product_id": p.get("product_id"),
            "name": p.get("title", "Unknown"),
            "category": p.get("category"),
            "price": p.get("price")
        })
    return {
        "total": len(products),
        "skip": skip,
        "limit": limit,
        "products": formatted_products
    }