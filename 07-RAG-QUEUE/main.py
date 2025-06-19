import uvicorn
from server import app
import multiprocessing

multiprocessing.set_start_method("spawn", force=True)

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)


