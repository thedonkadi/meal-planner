from langchain.tools import Tool
from app.retriever import RecipeRetriever

retriever = RecipeRetriever()

def ingredient_search_tool(query: str) -> str:
    results = retriever.search(query)

    if not results:
        return "No recipes found."

    output = ""
    for i, recipe in enumerate(results, start=1):
        output += f"\nResult {i}\n"
        output += f"Title: {recipe['title']}\n"
        output += f"Ingredients: {recipe['ingredients']}\n"

    return output


recipe_tool = Tool(
    name="RecipeSearch",
    func=ingredient_search_tool,
    description="Use this tool to find recipes based on ingredients or meal preferences."
)