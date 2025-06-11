from fastapi import FastAPI, Query, Response 
from config.worker import process_query
from config.connection import queue
from datetime import datetime
app = FastAPI()

@app.get("/")
async def root():
  return {
        "status_code":200,
        "success":"ok",
        "message": "Hello World"}
 
       
@app.post("/chat" )
async def chat(
    response: Response,
    query: str = Query(..., description="Chat Message")
    
):
    """
    Endpoint description
    """
    job  = queue.enqueue(process_query, query)
    response.headers["Custom-Header"] = "value"
    return  {"status":"queued", "job_id": job.id, "timestamp": datetime.now().isoformat()}


    
    