import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus

env_path = os.path.join(os.path.dirname(__file__), "mong.env")
load_dotenv(env_path)


MONGODB_URI = os.getenv("MONGODB_URI")
print(f"Debug: MONGODB_URI loaded: {'Yes' if MONGODB_URI else 'No'}")


client = MongoClient(MONGODB_URI)

db = client["PDFCHAT"]

chat_collection = db["chat_history"]

try:
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed")
    print(e)

def create_session(session_id, topicname):
    print("👍 Session_history Created")
    chat_collection.insert_one({
            "_id": session_id,
            "topic": topicname,
            "messages":[]
    })

def session_exists(session_id):
    return chat_collection.find_one({"_id": session_id}) is not None

def save_chat_turn(session_id, user_query, assistant_response):
    print("✌️ Saved RESPONSE and QUERY")
    result = chat_collection.update_one(
        {"_id": session_id},
        {
            "$push": {
                "messages": {
                    "$each": [
                        {
                            "role": "user",
                            "content": user_query
                        },
                        {
                            "role": "assistant",
                            "content": assistant_response
                        }
                    ]
                }
            }
        }
    )

    return result.modified_count == 1

def get_chat_history(session_id):
    print(">>>>>>>>>>>>>>Giving history to LLM")
    session = chat_collection.find_one(
        {"_id": session_id}
    )

    if session:
        return session["messages"]

    return []



