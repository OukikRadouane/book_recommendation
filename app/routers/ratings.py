from fastapi import APIRouter, HTTPException, Query
from app.services.mongodb_service import MongoDBService
from app.models.rating import RatingCreate, RatingResponse
from datetime import datetime

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=RatingResponse, status_code=201)
async def create_rating(rating: RatingCreate):
    """Ajoute une nouvelle note (rating) pour un utilisateur et un produit"""
    
    # Vérifier que le produit existe
    product = await MongoDBService.get_product(rating.product_id)
    if not product:
        raise HTTPException(
            status_code=404, 
            detail=f"Product {rating.product_id} not found"
        )
    
    # Créer le document rating
    rating_dict = {
        "user_id": rating.user_id,
        "product_id": rating.product_id,
        "rating": rating.rating,
        "timestamp": datetime.now()
    }
    
    # Insérer dans MongoDB
    created_rating = await MongoDBService.create_rating(rating_dict)
    
    return RatingResponse(
        user_id=created_rating["user_id"],
        product_id=created_rating["product_id"],
        rating=created_rating["rating"],
        timestamp=created_rating["timestamp"]
    )

@router.get("/user/{user_id}")
async def get_user_ratings(
    user_id: str,
    limit: int = Query(50, ge=1, le=500)
):
    """Récupère tous les ratings d'un utilisateur"""
    
    ratings = await MongoDBService.get_user_ratings(user_id, limit)
    
    if not ratings:
        return {
            "user_id": user_id,
            "ratings": [],
            "count": 0,
            "message": f"No ratings found for user {user_id}"
        }
    
    return {
        "user_id": user_id,
        "ratings": ratings,
        "count": len(ratings)
    }