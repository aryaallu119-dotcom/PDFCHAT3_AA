from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Request

from Rag_service.applogic import Rag_core


class PdfRequest(BaseModel):
    pdf_path: str
    topic: str
    session_id: str

class ResponseRequest(BaseModel):
    query: str
    status:str
    session_id: str

app = FastAPI()
PDF_PATH_FOR_RAG = None

@app.get("/")
def home():
    return{
        "message": "FastAPI is working...."
    }

@app.post("/process")
def process_pdf(data: PdfRequest):
    try:
        global PDF_PATH_FOR_RAG
        PDF_PATH_FOR_RAG = data.pdf_path
        print(data.topic)
        query_data ={
        "session_id": data.session_id,
        "query": "Greetings to you!",
        "status": True,
        "pdf_path": data.pdf_path,
        "topic_name": data.topic,
        }
        query_response = Rag_core(query_data)
        print(query_response)
        return {
            "response_msg": query_response,
            "sender": "bot",
            "pdf_path": data.pdf_path
        }
    except Exception as e:
        print(f"Error in /process endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "response_msg": f"Error processing PDF: {str(e)}",
            "sender": "error"
        }, 500
  
@app.post("/response")  
def query_response(data: ResponseRequest):
    try:
        query_data ={
        "query": data.query,
        "status": data.status
        }
        query_response = Rag_core(query_data)
        print(query_response)
        return {
            "response_msg": query_response,
            "sender": "bot"
        }
    except Exception as e:
        print(f"Error in /response endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "response_msg": f"Error processing query: {str(e)}",
            "sender": "error"
        }, 500
    
    

