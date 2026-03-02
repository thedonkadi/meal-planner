import sqlite3
import pandas as pd
from pathlib import Path


USDA_PATH = Path("data/usda_sr_legacy")

DB_PATH = "data/usda.db"

# Nutrient IDs we care about
IMPORTANT_NUTRIENTS = [
    1008,  # Energy (kcal)
    1003,  # Protein
    1004,  # Fat
    1005,  # Carbs
    1079,  # Fiber
    2000,  # Sugars
    1093   # Sodium
]


def build_database():
    print("Loading CSV files...")

    food = pd.read_csv(USDA_PATH / "food.csv")

    food = food[food["data_type"] == "sr_legacy_food"]
    food_nutrient = pd.read_csv(USDA_PATH / "food_nutrient.csv")
    nutrient = pd.read_csv(USDA_PATH / "nutrient.csv")



    food_nutrient = food_nutrient[
        food_nutrient["nutrient_id"].isin(IMPORTANT_NUTRIENTS)
    ]

    print("Creating SQLite database...")

    conn = sqlite3.connect(DB_PATH)

    food[["fdc_id", "description"]].to_sql(
        "food", conn, if_exists="replace", index=False
    )

    food_nutrient.to_sql(
        "food_nutrient", conn, if_exists="replace", index=False
    )

    nutrient[["id", "name", "unit_name"]].to_sql(
        "nutrient", conn, if_exists="replace", index=False
    )

    print("Creating indexes for speed...")

    conn.execute("CREATE INDEX idx_food_desc ON food(description)")
    conn.execute("CREATE INDEX idx_fn_fdc ON food_nutrient(fdc_id)")

    conn.commit()
    conn.close()

    print("✅ USDA database built successfully!")


if __name__ == "__main__":
    build_database()