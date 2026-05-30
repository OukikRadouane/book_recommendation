from pydantic import BaseModel
from typing import List
from datetime import datetime

class RecommendedProduct(BaseModel):
    """Un produit recommandé avec son score"""
    product_id: str
    score: float  # Score de recommandation (prédiction ALS)

class Recommendation(BaseModel):
    """Modèle de recommandations pour un utilisateur"""
    user_id: str
    recommendations: List[RecommendedProduct]
    generated_at: datetime

class RecommendationResponse(BaseModel):
    """Réponse API pour les recommandations"""
    user_id: str
    recommendations: List[RecommendedProduct]
    generated_at: datetime
    count: int  # Nombre de recommandations retournées