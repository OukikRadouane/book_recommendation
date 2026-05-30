import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

csv_file = BASE_DIR / "data" / "cleaned" / "books_cleaned_full.csv"
output_file = BASE_DIR / "data" / "synthetic" / "books_synthetic_10k.csv"
df = pd.read_csv(csv_file = csv_file)

synthetic_df = df.sample(
    n=10000,
    replace=True,
    random_state=42
)

synthetic_df.to_csv(
    output_file,
    index=False
)


print("10K synthetic dataset generated")