from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Rating(BaseModel):
    """Modèle complet d'un rating (pour lecture)"""
    user_id: str = Field(..., description="Identifiant unique de l'utilisateur")
    product_id: str = Field(..., description="Identifiant unique du produit")
    rating: float = Field(..., ge=0.0, le=5.0, description="Note de 0 à 5")
    timestamp: datetime = Field(default_factory=datetime.now, description="Date de la note")

class RatingCreate(BaseModel):
    """Modèle pour créer un rating (POST)"""
    user_id: str
    product_id: str
    rating: float = Field(..., ge=0.0, le=5.0)

class RatingResponse(BaseModel):
    """Modèle pour la réponse API d'un rating"""
    user_id: str
    product_id: str
    rating: float
    timestamp: datetime