from fastapi import FastAPI, Query, UploadFile, File 
from fastapi.responses import JSONResponse
from config.worker import process_query, load_data
from config.connection import queue
from datetime import datetime
import os
import shutil 


app = FastAPI()
UPLOAD_DIR = "uploaded_files"

# Ensure the directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)
@app.get("/")
async def root():
  return {
        "status_code":200,
        "success":"ok",
        "message": "Hello World"}
 

 # Wrapper for RQ
import asyncio 

def run_async_query(query: str):
    
    return asyncio.run(process_query(query))

@app.post("/chat" )
async def chat( 
    query: str = Query(..., description="Chat Message")
):
    """
    Endpoint description
    """
    job = queue.enqueue(run_async_query, query)
    return  {"status":"queued", "job_id": job.id, "timestamp": datetime.now().isoformat()}

 
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = await load_data(file_location)
    print(result)
    return JSONResponse({
        "filename": file.filename,
        "message": f"File saved to {file_location}"
    })
 