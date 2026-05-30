import pandas as pd
from pymongo import MongoClient
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

csv_file = BASE_DIR / "data" / "cleaned" / "books_cleaned_full.csv"

client = MongoClient(
    "mongodb+srv://teamuser:TeamPass123@book-recommendation-clu.1xxflfo.mongodb.net/?appName=book-recommendation-cluster"
)

db = client["book_recommendation_db"]

ratings = db["ratings"]
products = db["products"]

chunk_size = 2000
MAX_ROWS = 300000

total_rows = 0

for chunk in pd.read_csv(
    csv_file,
    chunksize=chunk_size
):

    total_rows += len(chunk)

    if total_rows > MAX_ROWS:
        break

    products_df = chunk[
        [
            "product_id",
            "title",
            "price"
        ]
    ].drop_duplicates()

    product_docs = []

    for _, row in products_df.iterrows():

        product_docs.append({
            "_id": str(row["product_id"]),
            "title": row["title"],
            "price": row["price"]
        })

    try:
        products.insert_many(
            product_docs,
            ordered=False
        )
    except:
        pass

    rating_docs = []

    for _, row in chunk.iterrows():

        rating_docs.append({
            "user_id": str(row["user_id"]),
            "product_id": str(row["product_id"]),
            "rating": float(row["rating"]),
            "timestamp": int(row["timestamp"])
        })

    try:
        ratings.insert_many(
            rating_docs,
            ordered=False
        )
    except:
        pass

    print(
        f"Processed {total_rows}"
    )

print("MongoDB seed completed")