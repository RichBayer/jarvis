#!/usr/bin/env python3

"""
NeuroCore Knowledge Retrieval Module

Responsibilities:
- Initialize embedding model and vector store (once)
- Provide fast retrieval interface
- Avoid heavy initialization at import time

This module is now controlled by the Runtime Manager.
"""

from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import chromadb


class KnowledgeBase:
    def __init__(self):
        """
        Initialize placeholders (no heavy loading yet)
        """
        self.retriever = None
        self.initialized = False

    def initialize(self):
        """
        Perform heavy initialization ONCE.
        """
        if self.initialized:
            return

        print("[Knowledge] Initializing embedding model and vector store...")

        embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        Settings.embed_model = embed_model

        chroma_client = chromadb.PersistentClient(
            path="/mnt/g/ai/memory/chroma"
        )

        collection = chroma_client.get_collection("jarvis_knowledge")

        vector_store = ChromaVectorStore(
            chroma_collection=collection
        )

        index = VectorStoreIndex.from_vector_store(vector_store)

        self.retriever = index.as_retriever(similarity_top_k=2)

        self.initialized = True

        print("[Knowledge] Initialization complete.")

    def retrieve(self, question: str) -> str:
        """
        Retrieve relevant knowledge.
        """
        if not self.initialized:
            self.initialize()

        results = self.retriever.retrieve(question)

        context = "\n\n".join(r.text for r in results)

        return context