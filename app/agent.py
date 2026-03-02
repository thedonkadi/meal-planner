import os
from groq import Groq
from app.retriever import RecipeRetriever

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
retriever = RecipeRetriever()


def run_agent(user_input: str):

    # Step 1: Ask LLM what to do
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are a recipe assistant. If user provides ingredients, extract them as a simple comma separated list."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0
    )

    extracted = response.choices[0].message.content.strip()

    print("\n[Agent extracted ingredients]:", extracted)

    # Step 2: Call your search tool
    results = retriever.search(extracted)

    if not results:
        return "No recipes found."

    output = ""
    for i, recipe in enumerate(results, start=1):
        output += f"\nResult {i}\n"
        output += f"Title: {recipe['title']}\n"
        output += f"Ingredients: {recipe['ingredients']}\n"

    return output