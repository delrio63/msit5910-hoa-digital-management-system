# tests/test_issues.py
from hoa_core import issues

def test_create_and_update_issue():
    issues._issues.clear()
    iid = issues.create_issue("Pothole", "Large pothole on 3rd", "alice")
    issues.assign_issue(iid, "maintenance")
    issues.update_issue_status(iid, "in_progress", "maintenance")
    listed = issues.list_issues({"reporter": "alice"})
    assert any(i["id"] == iid for i in listed)
    assert issues._issues[iid]["status"] == "in_progress"
