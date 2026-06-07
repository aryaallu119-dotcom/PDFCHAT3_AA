import os
from dotenv import load_dotenv
load_dotenv("new.env")
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# def getQueryResponse(pdf_path):
#     print("Received PDF:")
#     print(pdf_path)
#     return {
#         "message": "RAG processing completed",
#         "pdf_path": pdf_path
#     }


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

file_path = "......."
loader = PyPDFLoader(file_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)

all_splits = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

document_ids = vector_store.add_documents(documents=all_splits)

sample = vector_store.get(limit=1, include=["embeddings", "documents"])

model = init_chat_model(
    "google_genai:gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
)


def retrieve_context(query: str, k: int = 2):
    retrieved_docs = vector_store.similarity_search(query, k=k)

    docs_content = ""
    for doc in retrieved_docs:
        docs_content += f"Source: {doc.metadata}\n"
        docs_content += f"Content: {doc.page_content}\n\n"

    return docs_content, retrieved_docs


def ask_about_pdf(user_query):
    context, source_docs = retrieve_context(user_query, k=2)

    system_message = f"""You are a helpful chatbot.
Use only the following pieces of context to answer the question. Don't make up any new information:
{context}
"""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_query}
    ]

    response = model.invoke(messages)

    return {
        "answer": response.content,
        "source_documents": source_docs,
        "context_used": context
    }


result = ask_about_pdf(
    "What improvements have been made to attention mechanisms since 2017?"
)

print(result)
print(result["answer"])