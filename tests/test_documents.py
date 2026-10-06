# tests/test_documents.py
from hoa_core import documents

def test_upload_and_versioning():
    documents._docs.clear()
    doc_id = documents.upload_document("rules.pdf", b"content", "alice")
    latest = documents.get_latest_version(doc_id)
    assert latest["name"] == "rules.pdf"
    assert len(documents.list_versions(doc_id)) == 1

def test_validate_upload_limits():
    assert documents.validate_upload("a", b"x") is True
    assert documents.validate_upload("", b"x") is False
    assert documents.validate_upload("a", b"") is False