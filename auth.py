import streamlit as st

# Hard-coded users for prototype
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "board": {"password": "board123", "role": "board"},
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

def create_user(username: str, password: str, role: str) -> None:
    """Create a new user."""
    if username in USERS:
        raise ValueError("User already exists")

    USERS[username] = {
        "password": password,
        "role": role
    }

def list_users() -> list:
    """Return all users with their roles."""
    return [
        {"username": username, "role": user["role"]}
        for username, user in USERS.items()
    ]
