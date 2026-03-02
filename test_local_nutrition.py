import sqlite3

DB_PATH = "data/usda.db"

def search_food(name):
    conn = sqlite3.connect(DB_PATH)
    words = name.lower().split()

    query = "SELECT description FROM food WHERE "
    conditions = []
    params = []

    for word in words:
        conditions.append("LOWER(description) LIKE ?")
        params.append(f"%{word}%")

    query += " AND ".join(conditions)
    query += " LIMIT 5;"

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows


print(search_food("mutton"))