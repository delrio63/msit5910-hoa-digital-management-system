from hoa_core.auth import create_user, authenticate, get_role
from hoa_core.documents import upload_document, get_latest_version, list_versions
from hoa_core.issues import create_issue, assign_issue, update_issue_status, get_issue, list_issues
from hoa_core.messages import post_message, get_thread

print("=== AUTH TESTS ===")
create_user("alice", "password123", "admin")
print("Authenticate:", authenticate("alice", "password123"))
print("Role:", get_role("alice"))

print("\n=== DOCUMENT TESTS ===")
doc_id = upload_document("rules.pdf", b"content", "alice")
print("Doc ID:", doc_id)
print("Latest Version:", get_latest_version(doc_id))
print("All Versions:", list_versions(doc_id))

print("\n=== ISSUE TESTS ===")
issue_id = create_issue("Pothole", "Large pothole on 3rd", "alice")
assign_issue(issue_id, "maintenance")
update_issue_status(issue_id, "in_progress", "maintenance")
print("Issue:", get_issue(issue_id))
print("All Issues:", list_issues())

print("\n=== MESSAGE TESTS ===")
post_message("announcements", "alice", "Welcome to the HOA system!")
print("Thread:", get_thread("announcements"))
