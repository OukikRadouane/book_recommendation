from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class MongoDB:
    """Gestionnaire de connexion MongoDB asynchrone"""

    client: AsyncIOMotorClient = None
    database = None

    @classmethod
    async def connect(cls):
        """Établit la connexion à MongoDB"""
        cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
        cls.database = cls.client[settings.DATABASE_NAME]
        print(f"✅ Connecté à MongoDB: {settings.DATABASE_NAME}")

    @classmethod
    async def disconnect(cls):
        """Ferme la connexion MongoDB"""
        if cls.client:
            cls.client.close()
            print("✅ Déconnecté de MongoDB")

    @classmethod
    def get_db(cls):
        """Retourne l'instance de la base de données"""
        return cls.database
    
db = MongoDB()