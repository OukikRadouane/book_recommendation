from app.routers.health import router as health_router
from app.routers.products import router as products_router
from app.routers.recommendations import router as recommendations_router
from app.routers.ratings import router as ratings_router

__all__ = ["health_router", "products_router", "recommendations_router", "ratings_router"]