# hoa_core/messages.py
from typing import Dict, List
import uuid
from datetime import datetime, UTC

_threads: Dict[str, List[Dict]] = {}

def post_message(thread_id: str, author: str, text: str) -> str:
    if not text.strip():
        raise ValueError("Message cannot be empty")
    msg = {
        "id": str(uuid.uuid4()),
        "author": author,
        "text": text,
        "posted_at": datetime.now(UTC).isoformat()
    }   
    
    _threads.setdefault(thread_id, []).append(msg)
    return msg["id"]

def get_thread(thread_id: str) -> List[Dict]:
    return _threads.get(thread_id, [])