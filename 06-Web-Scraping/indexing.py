from pathlib import Path
from langchain_community.document_loaders import JsonLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

 
from langchain_openai import OpenAIEmbeddings   
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

load_dotenv()  # Load environment variables from .env file
# This code loads a PDF file, reads its content, and splits the text into chunks.

pdf_path = Path(__file__).parent / "scraped_data.json"  # Path to the PDF file
loader = JsonLoader(pdf_path)
documents = loader.load() #Read the PDF file

# print("Docs[0]", documents[5]) #Print the first document    

#chunking


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=300,
)

split_docs = text_splitter.split_documents(documents) #Split the documents into chunks
print("Split Docs[0]", split_docs[0]) #Print the first chunk of the split documents

#vector Embeddings 
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large") #Initialize the OpenAI embeddings model

# TODO: Add Qdrant integration code here if needed
vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="web_scraped_data",
    embedding=embedding_model
)
print("Indexing of Document Done...")