# hoa_core/documents.py

from typing import Dict, List
import uuid
from datetime import datetime, UTC

_docs: Dict[str, List[Dict]] = {}

def upload_document(name: str, content: bytes, uploader: str) -> str:
    doc_id = str(uuid.uuid4())
    version = {
        "version_id": str(uuid.uuid4()),
        "name": name,
        "content": content,
        "uploader": uploader,
        "uploaded_at": datetime.now(UTC).isoformat()
    }
    _docs.setdefault(doc_id, []).append(version)
    return doc_id

def get_latest_version(doc_id: str) -> Dict:
    versions = _docs.get(doc_id)
    if not versions:
        raise KeyError("Document not found")
    return versions[-1]

def list_versions(doc_id: str) -> List[Dict]:
    return _docs.get(doc_id, [])

def validate_upload(name: str, content: bytes) -> bool:
    if not name or not content:
        return False
    if len(content) > 10 * 1024 * 1024:  # 10 MB limit
        return False
    return True

def list_documents() -> list:
    """Return all documents with their latest version."""
    return [
        {
            "doc_id": doc_id,
            "name": versions[-1]["name"],
            "version_id": versions[-1]["version_id"],
            "uploaded_by": versions[-1]["uploader"],
            "timestamp": versions[-1]["uploaded_at"]
        }
        for doc_id, versions in _docs.items()
    ]


