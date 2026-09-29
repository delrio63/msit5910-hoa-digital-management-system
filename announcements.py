import json
import os
from datetime import datetime
import streamlit as st

# JSON file for persistent storage
DATA_FILE = os.path.join(os.path.dirname(__file__), "announcements_data.json")

def load_announcements():
    """Load announcements from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_announcements(announcements):
    """Save announcements to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(announcements, f, indent=4)

# Initialize session state from JSON
if "announcements" not in st.session_state:
    st.session_state.announcements = load_announcements()

def add_announcement(title, message, author):
    """Add a new announcement and persist it."""
    announcement = {
        "title": title,
        "message": message,
        "author": author,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    st.session_state.announcements.append(announcement)
    save_announcements(st.session_state.announcements)

def get_announcements():
    """Return all announcements."""
    return st.session_state.announcements

