from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import chromadb
import sys


# Configure embedding model (must match indexing configuration)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def retrieve_knowledge(question: str, top_k: int = 2) -> str:
    """
    Retrieve relevant knowledge chunks from the Jarvis Chroma database.
    """

    # Connect to persistent Chroma database
    chroma_client = chromadb.PersistentClient(
        path="/mnt/g/ai/memory/chroma"
    )

    # Load the Jarvis knowledge collection
    collection = chroma_client.get_collection("jarvis_knowledge")

    vector_store = ChromaVectorStore(
        chroma_collection=collection
    )

    # Rebuild index interface
    index = VectorStoreIndex.from_vector_store(vector_store)

    # Create retriever
    retriever = index.as_retriever(similarity_top_k=top_k)

    # Retrieve relevant chunks
    results = retriever.retrieve(question)

    # Combine retrieved text into a clean context block
    context = "\n\n".join(r.text for r in results)

    return context


# CLI compatibility (so the script can still run directly)
if __name__ == "__main__":

    question = " ".join(sys.argv[1:])

    if not question:
        print("Please provide a question.")
        sys.exit()

    context = retrieve_knowledge(question)

    print("\n--- Retrieved Knowledge Context ---\n")
    print(context)