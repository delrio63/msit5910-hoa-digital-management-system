# hoa_core/documents.py

import os
import json
import uuid
from datetime import datetime, UTC
from typing import Dict, List

# ---------------------------
# Storage locations
# ---------------------------
DATA_FILE = "documents_data.json"
DOCS_FOLDER = "documents_storage"

# Ensure folder exists
os.makedirs(DOCS_FOLDER, exist_ok=True)

# ---------------------------
# Load + Save
# ---------------------------
def _load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_data():
    """Persist document metadata to disk."""
    with open(DATA_FILE, "w") as f:
        json.dump(_docs, f, indent=4)

# In-memory cache (loaded from disk at startup)
_docs: Dict[str, List[Dict]] = _load_data()

# ---------------------------
# Upload document
# ---------------------------
def upload_document(file, name: str, uploader: str) -> str:
    """Store file on disk + store metadata in JSON + maintain versioning."""
    doc_id = name.lower().strip()

    version_id = str(uuid.uuid4())

    # Save file to disk
    file_path = os.path.join(DOCS_FOLDER, f"{version_id}_{name}")
    with open(file_path, "wb") as f:
        f.write(file.getvalue())

    # Metadata
    version = {
        "version_id": version_id,
        "name": name,
        "file_path": file_path,
        "uploader": uploader,
        "uploaded_at": datetime.now(UTC).isoformat()
    }

    # Add version to memory
    _docs.setdefault(doc_id, []).append(version)

    # Persist to disk
    _save_data()

    return doc_id

# ---------------------------
# Get latest version
# ---------------------------
def get_latest_version(doc_id: str) -> Dict:
    versions = _docs.get(doc_id)
    if not versions:
        raise KeyError("Document not found")
    return versions[-1]


# ---------------------------
# List all versions of a document
# ---------------------------
def list_versions(doc_id: str) -> List[Dict]:
    return _docs.get(doc_id, [])


# ---------------------------
# Validate upload
# ---------------------------
def validate_upload(name: str, content: bytes) -> bool:
    if not name or not content:
        return False
    if len(content) > 10 * 1024 * 1024:  # 10 MB limit
        return False
    return True


# ---------------------------
# List all documents (latest version only)
# ---------------------------
def list_documents() -> list:
    """Return all documents with their latest version."""
    return [
        {
            "doc_id": doc_id,
            "name": versions[-1]["name"],
            "version": len(versions),
            "version_id": versions[-1]["version_id"],
            "uploaded_by": versions[-1]["uploader"],
            "uploaded_at": versions[-1]["uploaded_at"],
            "file_path": versions[-1]["file_path"]
        }
        for doc_id, versions in _docs.items()
    ]
