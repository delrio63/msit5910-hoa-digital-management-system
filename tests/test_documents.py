# tests/test_documents.py
from hoa_core import documents
from io import BytesIO

def test_upload_and_versioning():
    documents._docs.clear()
    doc_id = documents.upload_document(
    BytesIO(b"content"),
    "rules.pdf",
    "alice"
)
    latest = documents.get_latest_version(doc_id)
    assert latest["name"] == "rules.pdf"
    assert len(documents.list_versions(doc_id)) == 1

def test_validate_upload_limits():
    assert documents.validate_upload("a.pdf", b"x") is True
    assert documents.validate_upload("", b"x") is False
    assert documents.validate_upload("a.pdf", b"") is False
    
    assert documents.validate_upload(
        "a.pdf",
        b"x" * (5 * 1024 * 1024)
    ) is True

    assert documents.validate_upload(
        "a.pdf",
        b"x" * (5 * 1024 * 1024 + 1)
    ) is False