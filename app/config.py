import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuration de l'application"""

    #mongodb
    MONGODB_URI:str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "ecommerce_recommendations")

    #API
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_TITLE: str = "E-commerce Recommendation API"
    API_VERSION: str = "1.0.0"

    #Collections MongoDB
    COLLECTION_RATINGS: str = "ratings"
    COLLECTION_PRODUCTS: str = "products"
    COLLECTION_RECOMMENDATIONS: str = "recommendations"

    # Pagination
    DEFAULT_LIMIT: int = 10
    MAX_LIMIT: int = 100

settings =Settings()