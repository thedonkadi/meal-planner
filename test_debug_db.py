import sqlite3

conn = sqlite3.connect("data/usda.db")

rows = conn.execute("""
SELECT id, name 
FROM nutrient
WHERE LOWER(name) IN ('energy', 'protein', 'total lipid (fat)', 'carbohydrate, by difference')
""").fetchall()

print(rows)
conn.close()