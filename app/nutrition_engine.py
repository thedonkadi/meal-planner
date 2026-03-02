import sqlite3

DB_PATH = "data/usda.db"

NUTRIENT_MAP = {
    "Energy": "calories",
    "Protein": "protein",
    "Total lipid (fat)": "fat",
    "Carbohydrate, by difference": "carbs",
    "Fiber, total dietary": "fiber",
    "Sugars, total including NLEA": "sugar",
    "Sodium, Na": "sodium"
}


def search_food(name):
    conn = sqlite3.connect(DB_PATH)

    words = name.lower().split()

    query = """
    SELECT fdc_id, description
    FROM food
    WHERE (
    """

    conditions = []
    params = []

    for word in words:
        conditions.append("LOWER(description) LIKE ?")
        params.append(f"%{word}%")

    query += " AND ".join(conditions)
    query += """
    )
    ORDER BY
        -- Penalize restaurant/branded foods
        CASE
            WHEN LOWER(description) LIKE '%applebee%' THEN 5
            WHEN LOWER(description) LIKE '%arby%' THEN 5
            WHEN LOWER(description) LIKE '%restaurant%' THEN 5
            WHEN LOWER(description) LIKE '%brand%' THEN 5
            ELSE 0
        END,

        -- Prefer raw
        CASE
            WHEN LOWER(description) LIKE '%raw%' THEN 0
            WHEN LOWER(description) LIKE '%cooked%' THEN 1
            ELSE 2
        END,

        LENGTH(description) ASC
    LIMIT 1;
    """

    row = conn.execute(query, params).fetchone()
    conn.close()

    return row


def get_nutrition_per_100g(fdc_id):
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT n.name, n.unit_name, fn.amount
    FROM food_nutrient fn
    JOIN nutrient n ON fn.nutrient_id = n.id
    WHERE fn.fdc_id = ?
    """

    rows = conn.execute(query, (fdc_id,)).fetchall()
    conn.close()

    nutrition = {
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "fiber": 0,
        "sugar": 0,
        "sodium": 0
    }

    for name, unit, amount in rows:
        # Filter only kcal for energy
        # Handle energy separately
        if "Energy" in name and unit == "kcal":
            nutrition["calories"] = amount
            continue

        if name in NUTRIENT_MAP:
            key = NUTRIENT_MAP[name]
            nutrition[key] = amount

    return nutrition


def calculate_nutrition(ingredient_name, grams):
    match = search_food(ingredient_name)

    if not match:
        return None

    fdc_id, description = match

    per_100g = get_nutrition_per_100g(fdc_id)

    result = {}
    for key, value in per_100g.items():
        result[key] = round((value / 100) * grams, 2)

    return {
        "matched_food": description,
        "nutrition": result
    }