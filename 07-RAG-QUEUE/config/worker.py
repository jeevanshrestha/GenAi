from pathlib import Path 
from config.db import Vectors 
from config.loader import load_pdf, load_json 
from openai import OpenAI 
import multiprocessing
 

multiprocessing.set_start_method('spawn')
 
client = OpenAI() 

vectors = Vectors()

async def process_query(query: str):
    
    print(query)
    
    return "Hello"
    
     
    
async def load_data(filepath: str):   
    print('File received', filepath, __name__)
    try:
        # check file type: if pdf load load_pdf, if json load load_json from loader
        file_ext = Path(filepath).suffix.lower() 
        if file_ext == ".pdf":
            split_docs = await load_pdf(filepath)
        elif file_ext == ".json":
            split_docs = await load_json(filepath)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        results = await vectors.save_to_database(split_docs)
        return results
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
        return None
    
    # Make sure to call load_data using 'await' in your async context, for example:
    # results = await load_data(filepath)