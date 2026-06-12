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
print(f"Debug: GROQ_API_KEY loaded: {'Yes' if GROQ_API_KEY else 'No'}")

def get_vector_store(topic_name, embeddings):
    """Load or create a persistent vector store for a topic from disk"""
    # Sanitize topic name for folder path
    safe_topic_name = topic_name.strip().lower()
    safe_topic_name = re.sub(r'[^a-z0-9\s]', '', safe_topic_name)  # Remove non-alphanumeric chars
    safe_topic_name = re.sub(r'\s+', '_', safe_topic_name)  # Replace spaces with underscores
    
    db_path = f"./chroma_langchain_db/{safe_topic_name}"
    
    # Check if database already exists on disk
    if os.path.exists(db_path):
        print(f"✓ LOADING EXISTING database from disk: {db_path}")
        print(f"  Collection name: {safe_topic_name}")
    else:
        print(f"✓ CREATING NEW database at: {db_path}")
        print(f"  Collection name: {safe_topic_name}")
    
    # Chroma automatically loads from disk if persist_directory exists
    # If it doesn't exist, Chroma creates a new one
    vector_store = Chroma(
        collection_name=safe_topic_name,
        embedding_function=embeddings,
        persist_directory=db_path,  # ← Chroma knows to save/load from this path
    )
    
    # Show current collection stats
    count = vector_store._collection.count() if hasattr(vector_store, '_collection') else "unknown"
    print(f"  Current documents in collection: {count}")
    
    return vector_store

def clean_response(text):
    """Remove <think> and </think> tags from LLM response"""
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned.strip()

def Rag_core(given_data):
    try:
        # Load embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        session_id = given_data.get("session_id", "default")
        print(f"got session_id:{session_id}")
        topic_name = given_data.get("topic_name", "default")
        print(f"Processing topic: {topic_name}")
        
        # Load/create persistent vector store for this topic
        vector_store = get_vector_store(topic_name, embeddings)
            
    except Exception as e:
        print(f"Error initializing vector store: {str(e)}")
        raise
    
        
    
    def Pdf_Indexing(file_path, vector_store):
        """
        Indexes a PDF file into the vector store.
        
        How it works:
        1. Load PDF from file_path
        2. Split text into chunks
        3. Create embeddings for each chunk
        4. Add to vector_store (which knows persist_directory from creation)
        5. Chroma automatically saves embeddings to disk
        """
        # Adjust path to work from python_services directory
        # If path doesn't exist, try with parent directory
        if not os.path.exists(file_path):
            adjusted_path = os.path.join("..", file_path)
            if os.path.exists(adjusted_path):
                file_path = adjusted_path
        
        print(f"\n📄 Processing PDF: {file_path}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        print(f"  ✓ Loaded {len(docs)} pages from PDF")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )

        all_splits = text_splitter.split_documents(docs)
        print(f"  ✓ Text split into {len(all_splits)} chunks")

        # add_documents() automatically saves to disk via persist_directory
        # The vector_store object "remembers" where to save because it was created
        # with persist_directory="./chroma_langchain_db/{topic_name}"
        print(f"\n→ Adding {len(all_splits)} document chunks to vector database...")
        document_ids = vector_store.add_documents(documents=all_splits)
        print(f"✓ SUCCESSFULLY added {len(document_ids)} documents")
        print(f"✓ Data automatically persisted to disk\n")
        
        sample = vector_store.get(limit=1, include=["embeddings", "documents"])

    if not GROQ_API_KEY:
        raise ValueError("GOOGLE_API_KEY not set in environment")
    
    model = init_chat_model(
        "groq:qwen/qwen3-32b",
        api_key=GROQ_API_KEY,
    )

    def Quering(input_query, vector_store):
        
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
            print(f"********************the input query is  {user_query}")
            system_message = f"""You are a helpful chatbot(PDFchart).
                                Use only the following pieces of context to answer the 
                                question. Don't make up any new information:{context} as
                                is drawn from Pdf uploaded by user."""

            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_query}
            ]
            print(messages)
            try:
                response = model.invoke(messages)
            except Exception as e:
                print(f"LLM model Error:{e}")
                raise  # Re-raise to handle at caller level

            return {
                "answer": response.content,
                "source_documents": source_docs,
                "context_used": context
            }

        return ask_about_pdf(input_query)

    try:
        if given_data.get("status") and "pdf_path" in given_data:
            print(f"Got session_id:{session_id}")
            # New PDF - index it
            print(f"Indexing PDF for topic: {topic_name}")
            Pdf_Indexing(given_data["pdf_path"], vector_store)
            result = Quering(given_data["query"], vector_store)
            # print(result)
            print(result["answer"])
            answer = clean_response(result["answer"])
            return answer
        elif "query" in given_data:
            # Query existing indexed PDF
            print(f"Querying topic: {topic_name}")
            result = Quering(given_data["query"], vector_store)
            # print(result["context_used"])
            print(result["answer"])
            answer = clean_response(result["answer"])
            
            return answer
        else:
            raise ValueError("Invalid request: must provide 'query' and optionally 'pdf_path'")
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise
    
