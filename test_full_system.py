from app.full_pipeline import AINutritionSystem

ai = AINutritionSystem()

result = ai.generate_meal_from_query("chicken, garlic")

if result:
    print("\n--- MEAL NUTRITION ---")
    for k, v in result["nutrition"].items():
        print(k, ":", round(v, 2))