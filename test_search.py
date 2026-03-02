from app.retriever import RecipeRetriever

retriever = RecipeRetriever()

query = input("Enter ingredients or meal preference: ")

results = retriever.search(query)

if not results:
    print("No recipes found.")
else:
    for i, recipe in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Title:", recipe["title"])
        print("Ingredients:", recipe["ingredients"])