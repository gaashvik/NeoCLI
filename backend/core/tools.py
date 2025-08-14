import faiss
from ..models import index_metadata
from huggingface_hub import InferenceClient
import numpy as np
from ..models import session
from langchain_core.tools import tool
from ..utilities import interupt
from ..configuration import config


MODEL_NAME= "BAAI/bge-large-en-v1.5"
client = InferenceClient(
    provider="hf-inference",
    model=MODEL_NAME,
    token=config.HUGGING_FACE_API
)


@tool
def retrieve_context(promt:str):
    '''used to search and return contextual infromation from codebase about project. use ONLY! if users ask project related questions. else use your own knowledge'''
    db=index_metadata.MetadataDB()
    def embed(text):
        """Use HF SDK to embed text"""
        try:
            return client.feature_extraction(text, normalize=True,truncate=True)
        except Exception as e:
            print(f"HF embedding failed: {e}")
            return None
    index = faiss.read_index(f"{config.META_DIR}/.neocli/chroma/faiss.index")
    print("made it here")
    emb = embed(promt)
    print("made it here even")
    emb = np.expand_dims(emb, axis=0)

    # perform similarity search
    D, I = index.search(emb, k=3)
    list=db.get_meta_for_vector_ids(I[0])
    contex=""
    for i,item in enumerate(list):
        with open (item[1],"r") as f:
            lines=f.readlines()
            contex+=(f"{i+1}. FilePath: {item[1]}\n   Start Line: {item[2]}\n   End Line: {item[3]}\n   Content:"+"".join(lines[item[2]:item[3]+1]))
        f.close()
        contex+=("\n-------------------------------------------\n")
        print("damn here as well")
    return contex

shell=session.ai_shell()
@tool
def run_shell_command(command : str) -> str:
    """Run bash shell commands. Input should be a valid shell command. and a single invocation can run a single command"""
    return shell.run(command)


tool_list=[interupt.add_human_in_the_loop(run_shell_command),retrieve_context]

