from app.meal_engine import calculate_meal_nutrition

recipe = {
    "title": "Pepper Chicken",
    "ingredients": [
        "tofu, 200g",
        "2 tbsp salt",
        "1 cup curd",
        "3 cloves garlic, minced"
    ]
}

result = calculate_meal_nutrition(recipe)

print("\nMEAL NUTRITION:")
for k, v in result.items():
    print(k, ":", round(v, 2))