from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://teamuser:TeamPass123@book-recommendation-clu.1xxflfo.mongodb.net/?appName=book-recommendation-cluster"
)

db = client["book_recommendation_db"]

print(
    "Products:",
    db.products.count_documents({})
)

print(
    "Ratings:",
    db.ratings.count_documents({})
)

missing = db.ratings.count_documents(
    {
        "rating": {
            "$exists": False
        }
    }
)

print(
    "Missing ratings:",
    missing
)