from app.database import db
from app.config import settings
from typing import List, Dict, Any, Optional
from datetime import datetime

class MongoDBService:
    """Service d'accès aux données MongoDB"""
    
    @staticmethod
    async def get_ratings_collection():
        """Retourne la collection ratings"""
        return db.get_db()[settings.COLLECTION_RATINGS]
    
    @staticmethod
    async def get_products_collection():
        """Retourne la collection products"""
        return db.get_db()[settings.COLLECTION_PRODUCTS]
    
    @staticmethod
    async def get_recommendations_collection():
        """Retourne la collection recommendations"""
        return db.get_db()[settings.COLLECTION_RECOMMENDATIONS]
    
    # ============ RATINGS ============
    
    @staticmethod
    async def create_rating(rating_data: dict) -> dict:
        """Ajoute un nouveau rating"""
        collection = await MongoDBService.get_ratings_collection()
        result = await collection.insert_one(rating_data)
        rating_data["_id"] = str(result.inserted_id)
        return rating_data
    
    @staticmethod
    async def get_user_ratings(user_id: str, limit: int = 50) -> List[dict]:
        """Récupère tous les ratings d'un utilisateur"""
        collection = await MongoDBService.get_ratings_collection()
        cursor = collection.find({"user_id": user_id}).limit(limit)
        ratings = await cursor.to_list(length=limit)
    
        for rating in ratings:
            # Convertir le timestamp entier en datetime
            if "timestamp" in rating and isinstance(rating["timestamp"], int):
                rating["timestamp"] = datetime.fromtimestamp(rating["timestamp"])
        
            # Convertir l'ObjectId en string
            if "_id" in rating:
                rating["_id"] = str(rating["_id"])
    
        return ratings
    
    # ============ PRODUCTS ============
    
    @staticmethod
    async def get_product(product_id: str) -> Optional[dict]:
        """Récupère un produit par son ID"""
        collection = await MongoDBService.get_products_collection()
        product = await collection.find_one({"_id": product_id})
        if product and "_id" in product:
            product["product_id"] = product.pop("_id")
    
        return product
    
    @staticmethod
    async def get_products_by_category(category: str, limit: int = 50) -> List[dict]:
        """Récupère les produits d'une catégorie"""
        collection = await MongoDBService.get_products_collection()
        cursor = collection.find({"category": category}).limit(limit)
        products = await cursor.to_list(length=limit)
        for product in products:
            if "_id" in product:
                product["product_id"] = product.pop("_id")
    
        return products
    
    @staticmethod
    async def get_all_products(skip: int = 0, limit: int = 100) -> List[dict]:
        """Récupère tous les produits (paginé)"""
        collection = await MongoDBService.get_products_collection()
        cursor = collection.find().skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)
        for product in products:
            if "_id" in product:
                product["product_id"] = product.pop("_id")
        return products
    
    # ============ RECOMMENDATIONS ============
    
    @staticmethod
    async def get_user_recommendations(user_id: str) -> Optional[dict]:
        """Récupère les recommandations pré-calculées pour un utilisateur"""
        collection = await MongoDBService.get_recommendations_collection()
        return await collection.find_one({"user_id": user_id})
    
    @staticmethod
    async def filter_recommendations_by_category(
        recommendations: List[dict], 
        category: str
    ) -> List[dict]:
        """Filtre les recommandations par catégorie (nécessite d'enrichir avec produits)"""
        products_collection = await MongoDBService.get_products_collection()
        
        filtered = []
        for rec in recommendations:
            product = await products_collection.find_one({"_id": rec["product_id"]})
            if product and product.get("category") == category:
                filtered.append(rec)
        return filtered