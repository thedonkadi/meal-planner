import faiss
import pickle
import re
import ast
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "data/recipes_10k.index"
META_PATH = "data/recipes_10k_metadata.pkl"


class RecipeRetriever:

    def __init__(self):
        print("Loading model...")
        self.model = SentenceTransformer("all-mpnet-base-v2")

        print("Loading FAISS index...")
        self.index = faiss.read_index(INDEX_PATH)

        print("Loading metadata...")
        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r"[^a-zA-Z\s]", " ", text)
        words = text.split()

        stop_words = {
            "cup", "cups", "tbsp", "tsp", "lb", "lbs",
            "oz", "ounce", "ounces", "clove", "cloves",
            "can", "cans", "pkg", "package",
            "chopped", "minced", "diced", "sliced",
            "fresh", "large", "small", "medium"
        }

        return set(word for word in words if word not in stop_words)

    def search(self, query, top_k=5):

        user_ingredients = [
            ing.strip().lower()
            for ing in query.split(",")
            if ing.strip()
        ]

        strict_matches = []

        for recipe in self.metadata:

            ingredients_field = recipe["ingredients"]

            if isinstance(ingredients_field, str):
                try:
                    ingredient_list = ast.literal_eval(ingredients_field)
                except:
                    ingredient_list = [ingredients_field]
            else:
                ingredient_list = ingredient_list = ingredients_field

            ingredients_text = " ".join(ingredient_list).lower()

            # ✅ Check each user ingredient appears somewhere
            if all(user_ing in ingredients_text for user_ing in user_ingredients):
                strict_matches.append(recipe)

            if len(strict_matches) >= top_k:
                break

        if strict_matches:
            print("Exact ingredient match found.\n")
            return strict_matches[:top_k]

        print("No exact ingredient match found. Showing semantic matches.\n")

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        return [self.metadata[idx] for idx in indices[0]]