import json
import os
from datetime import datetime
from uuid import uuid4
import streamlit as st

# JSON file for persistent storage
DATA_FILE = os.path.join(os.path.dirname(__file__), "announcements_data.json")


# ---------------------------------------------------------
# STORAGE MODEL (pending + published)
# ---------------------------------------------------------

def _load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        # If file is a list, convert to dict structure
        if isinstance(data, list):
            return {
                "pending": [],
                "published": data
            }

        # If keys are missing, add them
        if "pending" not in data:
            data["pending"] = []
        if "published" not in data:
            data["published"] = []

        return data

    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize empty structure if file missing or corrupted
        return {
            "pending": [],
            "published": []
        }

def _save_data(data):
    """Save announcements JSON safely."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------------------------------------
# Initialize session state
# ---------------------------------------------------------

def init_state():
    """Initialize announcements state safely inside Streamlit."""
    if "announcements_data" not in st.session_state:
        st.session_state.announcements_data = _load_data()

# ---------------------------------------------------------
# Board submits announcement (goes to pending)
# ---------------------------------------------------------

def submit_announcement(title: str, message: str, author: str) -> str:
    ann_id = str(uuid4())
    announcement = {
        "id": ann_id,
        "title": title,
        "message": message,
        "author": author,
        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    data = _load_data()

    data["pending"].append(announcement)

    _save_data(data)

    return ann_id


# ---------------------------------------------------------
# Admin publishes a pending announcement
# ---------------------------------------------------------

def publish_pending(ann_id: str, editor: str):
    """Admin publishes a pending announcement."""

    # Reload the latest data from disk
    data = _load_data() 
    pending = data["pending"]
    published = data["published"]

    for idx, ann in enumerate(pending):
        if ann["id"] == ann_id:

            published_ann = {
                "id": ann["id"],
                "title": ann["title"],
                "message": ann["message"],
                "published_by": editor,
                "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            published.append(published_ann)
            del pending[idx]

            _save_data(data)

            # Update session_state so UI reflects the new data
            st.session_state.announcements_data = data

            return

    raise KeyError(f"Pending announcement {ann_id} not found")


# ---------------------------------------------------------
# Admin edits a pending announcement
# ---------------------------------------------------------

from datetime import datetime

def edit_pending(ann_id: str, new_title: str, new_message: str, editor: str):
    data = _load_data()
    pending = data["pending"]

    for ann in pending:
        if ann["id"] == ann_id:
            ann["title"] = new_title
            ann["message"] = new_message
            ann["edited"] = True
            ann["edited_by"] = editor
            ann["edited_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _save_data(data)
            return

    raise KeyError(f"Pending announcement {ann_id} not found")

# ---------------------------------------------------------
# Admin adds announcement (append mode)
# ---------------------------------------------------------

def add_announcement(title: str, message: str, author: str) -> str:
    """Admin adds a new published announcement (append mode)."""
    ann_id = str(uuid4())
    announcement = {
        "id": ann_id,
        "title": title,
        "message": message,
        "author": author,
        "published_by": author,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    st.session_state.announcements_data["published"].append(announcement)
    _save_data(st.session_state.announcements_data)

    return ann_id

# ---------------------------------------------------------
# Admin replaces ALL published announcements
# ---------------------------------------------------------

def replace_announcements(title: str, message: str, author: str) -> str:
    """Admin replaces all published announcements with a single new one."""
    ann_id = str(uuid4())
    announcement = {
        "id": ann_id,
        "title": title,
        "message": message,
        "author": author,
        "published_by": author,
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Replace entire published list
    st.session_state.announcements_data["published"] = [announcement]
    _save_data(st.session_state.announcements_data)

    return ann_id

# ---------------------------------------------------------
# Getters for dashboards
# ---------------------------------------------------------

def get_pending():
    """Return all pending announcements."""
    return st.session_state.announcements_data["pending"]


def get_published():
    """Return all published announcements (newest first)."""
    return sorted(
        st.session_state.announcements_data["published"],
        key=lambda a: a.get("published_at", ""),
        reverse=True,
    )


# legacy compatibility
def get_announcements():
    """Legacy: return published announcements."""
    return get_published()

# ---------------------------------------------------------
# Delete helpers (Admin-only)
# ---------------------------------------------------------

def delete_pending(ann_id: str):
    """Admin deletes a pending announcement."""
    pending = st.session_state.announcements_data["pending"]
    st.session_state.announcements_data["pending"] = [
        ann for ann in pending if ann["id"] != ann_id
    ]
    _save_data(st.session_state.announcements_data)


def delete_published(ann_id: str):
    """Admin deletes a published announcement."""
    published = st.session_state.announcements_data["published"]
    st.session_state.announcements_data["published"] = [
        ann for ann in published if ann["id"] != ann_id
    ]
    _save_data(st.session_state.announcements_data)
