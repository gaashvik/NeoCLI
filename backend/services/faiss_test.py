import faiss
from backend.models.index_metadata import MetadataDB
from huggingface_hub import InferenceClient
from configuration import config
import numpy as np
db=MetadataDB()

MODEL_NAME= "BAAI/bge-large-en-v1.5"
client = InferenceClient(
    provider="hf-inference",
    model=MODEL_NAME,
    token=config.HUGGING_FACE_API
)
def embed(text):
    """Use HF SDK to embed text"""
    try:
        return client.feature_extraction(text, normalize=True,truncate=True)
    except Exception as e:
        print(f"HF embedding failed: {e}")
        return None

index = faiss.read_index("/home/shubhk/sentinal-ai/.neocli/chroma/faiss.index")

print("Number of vectors:", index.ntotal)

if isinstance(index, faiss.IndexIDMap):
    print("Stored IDs:", index.id_map)



import numpy as np

# create a random dummy query vector (same dimension as embedding)
query ="how is session being maintained for shell"
emb = embed(query)
emb = np.expand_dims(emb, axis=0)

# perform similarity search
D, I = index.search(emb, k=5)
print("Top 5 closest vector IDs:", I[0])
print("Distances:", D)

list=db.get_meta_for_vector_ids(I[0])

for item in list:
    with open (item[1],"r") as f:
        lines=f.readlines()
        print("File:"+item[1])
        print("".join(lines[item[2]:item[3]+1]))

