import requests
import uuid

def send_message_to_meta(message: str, conversation_id: str = "676664205534927"):
    url = "https://www.facebook.com/api/graphql/"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    request_id = str(uuid.uuid4())
    
    payload = {
        "doc_id": "24044662075146124",  # REPLACE with correct Meta doc_id
        "variables": {
            "message": message,
            "conversation_id": conversation_id,
            "client_mutation_id": request_id
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
