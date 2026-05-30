from fastapi import APIRouter, HTTPException, Query
from app.services.mongodb_service import MongoDBService
from app.models.recommendation import RecommendationResponse, RecommendedProduct

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/{user_id}", response_model=RecommendationResponse)
async def get_recommendations(
    user_id: str,
    category: str = Query(None, description="Filtrer les recommandations par catégorie"),
    limit: int = Query(10, ge=1, le=50, description="Nombre max de recommandations à retourner")
):
    """Récupère les recommandations pré-calculées pour un utilisateur"""
    
    # Récupérer les recommandations depuis MongoDB
    rec_data = await MongoDBService.get_user_recommendations(user_id)
    
    if not rec_data:
        raise HTTPException(
            status_code=404, 
            detail=f"No recommendations found for user {user_id}"
        )
    
    recommendations = rec_data.get("recommendations", [])
    
    # Filtrer par catégorie si demandé
    if category:
        recommendations = await MongoDBService.filter_recommendations_by_category(
            recommendations, category
        )
    
    # Limiter le nombre de résultats
    recommendations = recommendations[:limit]
    
    # Convertir en objets RecommendedProduct
    rec_objects = [
        RecommendedProduct(product_id=r["product_id"], score=r.get("score", 0.0))
        for r in recommendations
    ]
    
    return RecommendationResponse(
        user_id=user_id,
        recommendations=rec_objects,
        generated_at=rec_data.get("generated_at"),
        count=len(rec_objects)
    )