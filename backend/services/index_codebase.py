import os
import json
import hashlib
from tree_sitter import Parser,Language
import tree_sitter_python
import numpy as np
import tree_sitter_javascript
from huggingface_hub import InferenceClient
from configuration import config
import faiss
from metadata import MetadataDB
CODE_DIR = '/home/shubhk/sentinal-ai/'
ROOT_DIR ='/home/shubhk/sentinal-ai/.neocli/chroma'
CHUNK_SIZE = 20
MODEL_NAME= "BAAI/bge-large-en-v1.5"

os.makedirs(ROOT_DIR, exist_ok=True)

db = MetadataDB()

client = InferenceClient(
    provider="hf-inference",
    model=MODEL_NAME,
    token=config.HUGGING_FACE_API
)



LANGUAGE_GRAMMERS= {
    ".py":Language(tree_sitter_python.language()),
    ".js":Language(tree_sitter_javascript.language()),
}

CHUNK_NODES = {
    ".py":{"function_definition", "class_definition"},
    ".js":{"function_definition", "class_definition"},
}

parsers = {}
for ext,lang in LANGUAGE_GRAMMERS.items():
    parser=Parser(lang)
    parsers[ext]=parser

INDEX_FILE_PATH=ROOT_DIR+"/faiss.index"
embedding_dim = 1024  # intfloat/e5-small-v2
if os.path.exists(INDEX_FILE_PATH):
    index = faiss.read_index(INDEX_FILE_PATH)
else:
    base_index = faiss.IndexFlatL2(embedding_dim)
    index = faiss.IndexIDMap(base_index) 

def embed(text):
    """Use HF SDK to embed text"""
    try:
        return client.feature_extraction(text, normalize=True,truncate=True)
    except Exception as e:
        print(f"HF embedding failed: {e}")
        return None



seen_hashes={}
HASH_FILE_PATH=ROOT_DIR+"/hashes.json"

if os.path.exists(HASH_FILE_PATH):
    with open(HASH_FILE_PATH) as f:
        seen_hashes=json.load(f)

def hash_file(path):
    with open(path,"rb") as f:
        return hashlib.md5(f.read()).hexdigest()
    
    
def extracts_chunks(source_code, parser, chunk_types):
    tree =  parser.parse(source_code.encode("utf8"))
    root = tree.root_node
    chunks = []

    def walk(node):
        if node.type in chunk_types:
            code = source_code[node.start_byte:node.end_byte]
            chunks.append((code, node.start_point[0], node.end_point[0]))
        for child in node.children:
            walk(child)
    walk(root)
    return chunks
EXCLUDE_DIRS = {".venv", ".git", "__pycache__", "node_modules", "dist", "build", ".mypy_cache"}
def find_and_show_chunks():
    
    for root,dirs,files in os.walk(CODE_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            ext=os.path.splitext(fname)[1]
            if ext not in parsers:
                continue

            file_path=os.path.join(root,fname)
            file_hash=hash_file(file_path)
            if seen_hashes.get(file_path)==file_hash:
                continue

            if file_path in seen_hashes:
                old_ids=db.get_vector_ids_by_path(file_path)
                id_array = np.ascontiguousarray(np.array(old_ids, dtype='int64'))

                if old_ids:
                    db.remove_by_path(file_path)
                    index.remove_ids(faiss.IDSelectorArray(len(old_ids), faiss.swig_ptr(id_array)))
            try:
                with open(file_path,"r", encoding="utf8", errors="ignore") as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file_path}:{e}")
                continue
            print(f"\n File:{file_path}")
            parser=parsers[ext]
            chunk_types= CHUNK_NODES[ext]
            chunks=extracts_chunks(content,parser, chunk_types)
            if not chunks:
                continue
            print(f"Indexing {fname} ({len(chunks)} chunks)")
            for code_chunk, start, end in chunks:
                emb = embed(code_chunk)
                if emb is None:
                    print(f"Couldn't create emebedding for chunk of file path-:{file_path}")
                    continue
                emb = np.expand_dims(emb, axis=0)

                hash_input = f"{file_path}:{start}-{end}"
                vector_id = int(hashlib.sha256(hash_input.encode()).hexdigest(), 16) % (2**63)

                index.add_with_ids(emb,np.array([vector_id], dtype="int64"))
                db.add_chunk(vector_id,file_path,start,end)
            seen_hashes[file_path]=file_hash
    with open(HASH_FILE_PATH,"w") as f:
        json.dump(seen_hashes,f,indent=2)

    
    faiss.write_index(index,INDEX_FILE_PATH)
    db.close()
    print("Indexing complete")



if __name__ == "__main__":
    print(f"Extracting chunks from: {CODE_DIR}")
    find_and_show_chunks()