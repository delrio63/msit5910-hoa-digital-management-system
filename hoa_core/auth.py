# hoa_core/auth.py
import hashlib
import hmac
import secrets
from typing import Dict, Optional

_users: Dict[str, Dict] = {}

def _hash_password(password: str, salt: Optional[str] = None) -> Dict[str, str]:
    salt = salt or secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return {"salt": salt, "hash": hashed.hex()}

def create_user(username: str, password: str, role: str = "homeowner") -> None:
    if username in _users:
        raise ValueError("User already exists")
    pw = _hash_password(password)
    _users[username] = {"password": pw, "role": role}

def authenticate(username: str, password: str) -> bool:
    user = _users.get(username)
    if not user:
        return False
    return verify_password(username, password)

def verify_password(username: str, password: str) -> bool:
    user = _users.get(username)
    if not user:
        return False
    salt = user["password"]["salt"]
    expected = user["password"]["hash"]
    candidate = _hash_password(password, salt)["hash"]
    return hmac.compare_digest(candidate, expected)

def get_role(username: str) -> Optional[str]:
    user = _users.get(username)
    return user["role"] if user else None

def authorize(username: str, allowed_roles: list) -> bool:
    role = get_role(username)
    return role in allowed_roles