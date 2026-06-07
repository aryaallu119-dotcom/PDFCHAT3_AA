from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request

from Rag_service.applogic import getQueryResponse



class QueryRequest(BaseModel):
    query: str

app = FastAPI()
PDF_PATH_FOR_RAG = None

@app.get("/")
def home():
    return{
        "message": "FastAPI is working...."
    }

@app.post("/process")
def process_pdf(data: PdfRequest):
    global PDF_PATH_FOR_RAG
    PDF_PATH_FOR_RAG = data.pdf_path

    getQueryResponse(PDF_PATH_FOR_RAG)
    return {
        "query_response": PDF_PATH_FOR_RAG
    }
  
@app.post("/response")  
def query_response(data: QueryRequest):
    query = data.query
    

