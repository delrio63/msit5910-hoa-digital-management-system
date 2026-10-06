# hoa_core/issues.py

from typing import Dict
import uuid
from datetime import datetime, UTC

_issues: Dict[str, Dict] = {}

def create_issue(title: str, description: str, created_by: str) -> str:
    issue_id = str(uuid.uuid4())
    issue = {
        "id": issue_id,
        "title": title,
        "description": description,
        "reporter": created_by,
        "created_at": datetime.now(UTC).isoformat(),
        "status": "open",
        "history": []
    }
    _issues[issue_id] = issue
    return issue_id

def assign_issue(issue_id: str, assignee: str) -> None:
    if issue_id not in _issues:
        raise KeyError("Issue not found")
    _issues[issue_id]["assignee"] = assignee

def update_issue_status(issue_id: str, status: str, actor: str) -> None:
    if issue_id not in _issues:
        raise KeyError("Issue not found")

    _issues[issue_id]["status"] = status
    _issues[issue_id]["history"].append({
        "status": status,
        "updated_by": actor,
        "at": datetime.now(UTC).isoformat()
    })

def get_issue(issue_id: str) -> Dict:
    if issue_id not in _issues:
        raise KeyError("Issue not found")
    return _issues[issue_id]

def list_issues(filter_by: dict | None = None):
    results = list(_issues.values())
    if not filter_by:
        return results

    def matches(issue):
        for key, value in filter_by.items():
            if issue.get(key) != value:
                return False
        return True

    return [i for i in results if matches(i)]


