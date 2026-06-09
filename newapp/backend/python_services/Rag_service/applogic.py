import os
from dotenv import load_dotenv
import re
import shutil

# Load environment variables from the correct path
env_path = os.path.join(os.path.dirname(__file__), "app.env")
load_dotenv(env_path)

from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"Debug: GOOGLE_API_KEY loaded: {'Yes' if GROQ_API_KEY else 'No'}")
vector_store = None

def clean_response(text):
    """Remove <think> and </think> tags from LLM response"""
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned.strip()

def Rag_core(given_data):
    global vector_store
    
    try:
        # Load embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # If new PDF is being indexed, clear old data
        if given_data.get("status") and "pdf_path" in given_data:
            print("New PDF session detected - clearing old vector store...")
            # Delete the persistent database directory
            db_path = "./chroma_langchain_db"
            if os.path.exists(db_path):
                try:
                    shutil.rmtree(db_path)
                    print(f"Deleted old database at {db_path}")
                except Exception as e:
                    print(f"Could not delete database: {e}")
            
            if vector_store is not None:
                try:
                    vector_store.delete_collection()
                except:
                    pass
            vector_store = None
        
        # Initialize vector store (create if doesn't exist)
        if vector_store is None:
            print("Initializing fresh vector store...")
            vector_store = Chroma(
                collection_name="input_collection",
                embedding_function=embeddings,
                persist_directory="./chroma_langchain_db",
            )
    except Exception as e:
        print(f"Error initializing vector store: {str(e)}")
        raise
    
        
    
    def Pdf_Indexing(file_path):
        # Adjust path to work from python_services directory
        # If path doesn't exist, try with parent directory
        if not os.path.exists(file_path):
            adjusted_path = os.path.join("..", file_path)
            if os.path.exists(adjusted_path):
                file_path = adjusted_path
        
        print(f"Processing PDF: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )

        all_splits = text_splitter.split_documents(docs)

        global vector_store
        if vector_store is None:
            raise RuntimeError("Vector store not initialized")
        document_ids = vector_store.add_documents(documents=all_splits)
        sample = vector_store.get(limit=1, include=["embeddings", "documents"])

    if not GROQ_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in environment")
    
    model = init_chat_model(
        "groq:qwen/qwen3-32b",
        api_key=GROQ_API_KEY,
    )

    def Quering(input_query):
        global vector_store
        
        def retrieve_context(query: str, k: int = 5):
            retrieved_docs = vector_store.similarity_search(query, k=k)

            docs_content = ""
            for doc in retrieved_docs:
                docs_content += f"Source: {doc.metadata}\n"
                docs_content += f"Content: {doc.page_content}\n\n"

            return docs_content, retrieved_docs


        def ask_about_pdf(user_query):
            context, source_docs = retrieve_context(user_query, k=5)
            # print(f"the pdf lines are {context}")
            print(f"t********************the input query is  {user_query}")
            system_message = f"""You are a helpful chatbot(PDFchart).
                                Use only the following pieces of context to answer the 
                                question. Don't make up any new information:{context} as
                                is drawn from Pdf uploaded by user."""

            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_query}
            ]
            try:
                response = model.invoke(messages)
            except Exception as e:
                print(f"LLM model Error:{e}")
                
            

            return {
                "answer": response.content,
                "source_documents": source_docs,
                "context_used": context
            }


        return ask_about_pdf(input_query)

    try:
        if given_data.get("status") and "pdf_path" in given_data:
            # New PDF - index it
            Pdf_Indexing(given_data["pdf_path"])
            result = Quering(given_data["query"])
            # print(result)
            print(result["answer"])
            answer = clean_response(result["answer"])
            return answer
        elif "query" in given_data:
            # Query existing indexed PDF
            result = Quering(given_data["query"])
            # print(result["context_used"])
            print(result["answer"])
            answer = clean_response(result["answer"])
            return answer
        else:
            raise ValueError("Invalid request: must provide 'query' and optionally 'pdf_path'")
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise
    
