# tests/test_messages.py
from hoa_core import messages
import pytest

def test_post_and_get_thread():
    messages._threads.clear()
    tid = "announcements"
    mid = messages.post_message(tid, "alice", "Welcome")
    thread = messages.get_thread(tid)
    assert any(m["id"] == mid for m in thread)

def test_empty_message_rejected():
    messages._threads.clear()
    with pytest.raises(ValueError):
        messages.post_message("t1", "bob", "   ")