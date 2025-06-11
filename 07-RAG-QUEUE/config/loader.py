from pathlib import Path
import json 

from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
 
class Vectors:
    def __init__(self):
        self.collection_name = "learning_vectors"
        self.qdrant_url = "http://localhost:6333"

async  def load_pdf(pdf_path: str):

        print('File loading', pdf_path, __name__)
        """Load PDF and return split documents"""
        loader = PyPDFLoader(file_path=pdf_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return splitter.split_documents(documents)
    
async  def load_json(json_path: str):


        print('File loading', json_path, __name__)
        """Load JSON and return split documents"""
        with open(json_path, 'r') as f:
            data = json.load(f)

        docs = [
            Document(
                page_content=item["content"],
                metadata={"url": item["url"], "heading": item["heading"]}
            )
            for item in data
        ]

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return splitter.split_documents(docs)