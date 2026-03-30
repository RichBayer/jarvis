from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import chromadb
import sys

# ----------------------------
# GLOBAL INITIALIZATION (RUNS ONCE)
# ----------------------------

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

Settings.embed_model = embed_model

# Connect to Chroma once
chroma_client = chromadb.PersistentClient(
    path="/mnt/g/ai/memory/chroma"
)

collection = chroma_client.get_collection("jarvis_knowledge")

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

# Build index ONCE
index = VectorStoreIndex.from_vector_store(vector_store)

# Create retriever ONCE
retriever = index.as_retriever(similarity_top_k=2)


# ----------------------------
# FAST QUERY FUNCTION
# ----------------------------

def retrieve_knowledge(question: str) -> str:
    """
    Retrieve relevant knowledge chunks quickly (no re-init)
    """

    results = retriever.retrieve(question)

    context = "\n\n".join(r.text for r in results)

    return context


# CLI support
if __name__ == "__main__":

    question = " ".join(sys.argv[1:])

    if not question:
        print("Please provide a question.")
        sys.exit()

    context = retrieve_knowledge(question)

    print("\n--- Retrieved Knowledge Context ---\n")
    print(context)