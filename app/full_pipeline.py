from app.retriever import RecipeRetriever
from app.meal_engine import calculate_meal_nutrition


class AINutritionSystem:

    def __init__(self):
        self.retriever = RecipeRetriever()

    def generate_meal_from_query(self, query):

        recipes = self.retriever.search(query, top_k=1)

        if not recipes:
            print("No recipes found.")
            return None

        recipe = recipes[0]

        print("\nSelected Recipe:", recipe["title"])
        print("\nIngredients:")
        for ing in recipe["ingredients"]:
            print("-", ing)

        meal_nutrition = calculate_meal_nutrition(recipe)

        return {
            "title": recipe["title"],
            "ingredients": recipe["ingredients"],
            "nutrition": meal_nutrition
        }