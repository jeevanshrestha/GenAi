from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

 
from langchain_openai import OpenAIEmbeddings   
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

load_dotenv()  # Load environment variables from .env file
# This code loads a PDF file, reads its content, and splits the text into chunks.

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large") #Initialize 

class Embedding:

    def __init__(self) -> None:
        pass

    def save_to_database(self, dbname):
        vector_store = QdrantVectorStore.from_documents(
                        documents=split_docs,
                        url="http://localhost:6333",
                        collection_name="learning_vectors",
                        embedding=embedding_model
                    )
    
    def embed_query(self, query):
        vector_db = QdrantVectorStore.from_existing_collection(
            url="http://localhost:6333",
            collection_name="learning_vectors",
            embedding=embedding_model
        )