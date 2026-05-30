from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """Vérifie que l'API est opérationnelle"""
    return {"status": "ok", "message": "Recommendation API is running"}

@router.get("/")
async def root():
    """Endpoint racine"""
    return {
        "api": "E-commerce Recommendation API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }