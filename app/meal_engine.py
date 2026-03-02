from app.ingredient_parser import parse_ingredient
from app.unit_converter import convert_to_grams
from app.nutrition_engine import calculate_nutrition


def calculate_meal_nutrition(recipe):
    total = {
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "fiber": 0,
        "sugar": 0,
        "sodium": 0
    }

    for item in recipe["ingredients"]:
        parsed = parse_ingredient(item)

        grams = convert_to_grams(
            parsed["quantity"],
            parsed["unit"],
            parsed["ingredient"]
        )

        if grams is None:
            continue

        result = calculate_nutrition(parsed["ingredient"], grams)

        if result is None:
            continue

        for key in total:
            total[key] += result["nutrition"].get(key, 0)

    return total