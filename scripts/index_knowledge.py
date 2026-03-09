from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import chromadb

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load documents from the knowledge directory
documents = SimpleDirectoryReader("/mnt/g/ai/memory/knowledge").load_data()

# Start the Chroma client
chroma_client = chromadb.Client()

# Create a collection for Jarvis knowledge
collection = chroma_client.create_collection("jarvis_knowledge")

# Connect LlamaIndex to Chroma
vector_store = ChromaVectorStore(chroma_collection=collection)

# Build the index
index = VectorStoreIndex.from_documents(
    documents,
    vector_store=vector_store
)

print("Knowledge indexed successfully.")