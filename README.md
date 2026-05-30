# E-commerce Recommendation API

API REST pour un moteur de recommandation basé sur ALS (Spark MLlib).

## Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/health` | Vérification de l'API |
| GET | `/products/{id}` | Détail d'un produit |
| GET | `/products/` | Liste des produits |
| GET | `/recommendations/{user_id}` | Recommandations pour un utilisateur |
| POST | `/ratings/` | Ajouter une note |
| GET | `/ratings/user/{user_id}` | Notes d'un utilisateur |

## Installation

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload