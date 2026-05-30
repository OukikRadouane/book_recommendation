from fastapi import FastAPI
from app.config import settings
from app.database import db
from app.routers import health_router, products_router, recommendations_router, ratings_router

# Créer l'application FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API REST pour un moteur de recommandation e-commerce (ALS collaborative filtering)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============ Événements de cycle de vie ============

@app.on_event("startup")
async def startup_event():
    """Au démarrage : connexion à MongoDB"""
    await db.connect()
    print(f"✅ API {settings.API_TITLE} démarrée")

@app.on_event("shutdown")
async def shutdown_event():
    """À l'arrêt : fermeture de MongoDB"""
    await db.disconnect()
    print("🛑 API arrêtée")

# ============ Enregistrement des routes ============

app.include_router(health_router)
app.include_router(products_router)
app.include_router(recommendations_router)
app.include_router(ratings_router)