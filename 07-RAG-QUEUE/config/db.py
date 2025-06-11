from pathlib import Path
import json
import os
from dotenv import load_dotenv
import asyncio
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
load_dotenv()  # Load environment variables from .env file

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")  # Requires OPENAI_API_KEY

collection_name = os.environ.get('COLLECTION_NAME') or "default"


class Vectors:
    def __init__(self):
        self.qdrant_url = os.environ.get('QDRANT_URL') or "http://localhost:6333" 

    async    def save_to_database(self, split_docs):
            print("Chunks received", __name__)
            """Embed and store documents in Qdrant"""
            try:
                vector_store = await QdrantVectorStore.from_documents(
                    documents=split_docs,
                    url=self.qdrant_url,
                    collection_name=collection_name,
                    embedding=embedding_model
                )
                meta_data = [doc.metadata for doc in split_docs]
                return {
                    "success": True,
                    "message": f"Stored {len(split_docs)} chunks into Qdrant.",
                    "meta_data": meta_data
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Failed to store documents: {str(e)}",
                    "meta_data": []
                }


async    def search_query(self, query: str):
        print("Query received", __name__)
        """Search Qdrant for similar chunks"""
        vector_db = await QdrantVectorStore.from_existing_collection(
            url=self.qdrant_url,
            collection_name= collection_name,
            embedding=embedding_model
        )
        results = vector_db.similarity_search(query, k=3)
        for r in results:
            print(f"Score: (approx), Text: {r.page_content[:100]}")
            print("-" * 60)
 