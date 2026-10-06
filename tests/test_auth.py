# tests/test_auth.py
import pytest
from hoa_core import auth

def test_create_and_verify_user():
    auth._users.clear()
    auth.create_user("alice", "s3cret", role="admin")
    assert auth.verify_password("alice", "s3cret") is True
    assert auth.get_role("alice") == "admin"
    assert auth.authorize("alice", ["admin"]) is True

def test_duplicate_user_raises():
    auth._users.clear()
    auth.create_user("bob", "pw")
    with pytest.raises(ValueError):
        auth.create_user("bob", "pw2")