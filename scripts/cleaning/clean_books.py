import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
df = pd.read_csv("C:\\Users\\ilyas\\Downloads\\Books_rating.csv")
output_file = BASE_DIR / "data" / "cleaned" / "books_cleaned_full.csv"
df = df.dropna(subset=[
    "user_id",
    "product_id",
    "rating"
])

df = df.drop_duplicates()

df["rating"] = df["rating"] / 5.0

df.to_csv(
    output_file,
    index=False
)

print("Cleaning completed")
print("Rows:", len(df))