import os
import json
from dotenv import load_dotenv
from pprint import pprint
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
from pymongo import MongoClient

#Saved upto here 143
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"Debug: GROQ_API_KEY loaded: {'Yes' if GROQ_API_KEY else 'No'}")
chat_session = {}

def save_chat_history(session_id, messages):

    filepath = f"./chat_history/{session_id}.json"

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            messages,
            file,
            ensure_ascii=False,
            indent=4
        )


def load_chat_history(session_id):

    filepath = f"./chat_history/{session_id}.json"

    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

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
        print(f"got session_id: {session_id}")

        history = load_chat_history(session_id)
        recent_history = history[-2:]
        print(f"Recent history:{recent_history}")
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
            system_message = f"""You are a helpful PDF Chatbot.with No hallucinations, only provided contex content as response.

                                    Use the provided PDF context to answer user questions accurately.

                                    If the user asks a question that can be answered from the PDF context, answer using the context.

                                    If the user asks a follow-up question, use the conversation history to understand the reference, but answer based on the PDF context.

                                    If the PDF does not contain enough information to answer the question, politely say that the information was not found in the 
                                    uploaded PDF.(initially inform its not there in provided contex and bring back to given context again and dont ask for new context(ignore it))

                                    Do not make up facts that are not supported by the PDF context.(halucinate)
                                    try to extend the convo within contex for further assistance(only inside pdf context)
                                    Don't make up any new information:
                                Context:
                                {context}"""

            messages = [
                {"role": "system", "content": system_message}
                # {"role": "user", "content": user_query}
            ]

            messages.extend(recent_history)
            messages.append(
                {
                    "role": "user",
                    "content": user_query
                }
            )

            # pprint(messages)

            try:
                response = model.invoke(messages)
            except Exception as e:
                print(f"LLM model Error:{e}")
                raise  # Re-raise to handle at caller level
            
            answer = clean_response(response.content)
            history.extend([
                {
                    "role": "user",
                    "content": user_query
                },
                {
                    "role": "assistant",
                    "content": answer
                }
            ])

            save_chat_history(
                session_id,
                history
            )
            # pprint(f"chart Session:{chat_session}")


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
            print(f"Got session_id in query:{session_id}")

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
    
