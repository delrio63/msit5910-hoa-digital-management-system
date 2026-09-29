import streamlit as st

# Hard-coded users for prototype
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "board": {"password": "board123", "role": "board_member"},
    "resident": {"password": "resident123", "role": "resident"}
}


def login(username, password):
    """Validate username and password."""
    user = USERS.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None


def logout():
    """Clear session state."""
    for key in ["logged_in", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]
