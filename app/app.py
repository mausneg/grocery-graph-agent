from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.graph_data import graph_data
from app.graph_query import graph_query

app = FastAPI()

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})

@app.post("/ingest")
def ingest_data(data_path: str):
    try:
        result = graph_data.invoke({"data_path": data_path})
        return JSONResponse(content={"success": True, "result": result})
    except Exception as e:
        return JSONResponse(content={"success": False, "error_message": str(e)}, status_code=500)
    
@app.post("/query")
def query_data(question: str):
    try:
        result = graph_query.invoke({"question": question})
        return JSONResponse(content={"success": True, "result": result})
    except Exception as e:
        return JSONResponse(content={"success": False, "error_message": str(e)}, status_code=500)