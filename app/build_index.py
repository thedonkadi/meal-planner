import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

DATA_PATH = "data/recipes.csv"
INDEX_PATH = "data/recipes_10k.index"
META_PATH = "data/recipes_10k_metadata.pkl"

CHUNK_SIZE = 2000
MAX_ROWS = 10000
BATCH_SIZE = 128

print("Loading embedding model...")
model = SentenceTransformer("all-mpnet-base-v2")

dimension = 768
index = faiss.IndexFlatL2(dimension)

metadata = []
total_processed = 0

print("Processing recipes...\n")

for chunk in pd.read_csv(DATA_PATH, chunksize=CHUNK_SIZE):

    remaining = MAX_ROWS - total_processed
    if remaining <= 0:
        break

    chunk = chunk.head(remaining)

    # Embed ONLY title + ingredients
    chunk["combined"] = (
        chunk["title"].fillna("") + ". " +
        chunk["ingredients"].fillna("")
    )

    texts = chunk["combined"].tolist()

    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    index.add(embeddings.astype("float32"))

    metadata.extend(
        chunk[["title", "ingredients", "directions"]].to_dict("records")
    )

    total_processed += len(chunk)
    print(f"Indexed: {total_processed}/{MAX_ROWS}")

print("\nSaving FAISS index...")
faiss.write_index(index, INDEX_PATH)

print("Saving metadata...")
with open(META_PATH, "wb") as f:
    pickle.dump(metadata, f)

print("\n✅ Index built successfully!")