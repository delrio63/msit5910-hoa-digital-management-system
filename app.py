import streamlit as st
import announcements
from hoa_core import auth, documents, issues, messages

st.set_page_config(page_title="HOA Digital Management System", layout="wide")

# ---------------------------
# LOGIN SCREEN
# ---------------------------
def login_screen():
    st.title("HOA Digital Management System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if auth.authenticate(username, password):
            st.session_state["user"] = username
            st.session_state["role"] = auth.get_role(username)
            st.success(f"Welcome, {username}!")
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Invalid username or password")


# ---------------------------
# RESIDENT DASHBOARD
# ---------------------------
def resident_dashboard():
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("HOA System")
    st.sidebar.write(f"Logged in as: **{st.session_state['user']}**")
    st.sidebar.write(f"Role: **{st.session_state['role']}**")

    menu = ["Home", 
            "Announcements", 
            "Submit Issue or Maintenance Request", 
            "My Requests",  
            "Logout"
    ]
    choice = st.sidebar.radio("Navigation", menu)

    # --- PERSISTENT HEADER (copied from app_old.py) ---
    st.title("HOA Digital Management System")
    st.write("Initial prototype – Unit 4 implementation demo.")

    st.success(f"Welcome, {st.session_state['user']}!")
    st.write(f"Your role: **{st.session_state['role']}**")
    st.divider()

    # --- LOGOUT HANDLER ---
    if choice == "Logout":
        st.session_state.clear()
        st.rerun()

    # --- HOME SECTION ---
    if choice == "Home":
        st.header("Resident Dashboard")
        st.write("Use the sidebar to navigate.")

    # --- ANNOUNCEMENTS SECTION --- 
    elif choice == "Announcements":
        st.subheader("Community Announcements")

        all_anns = announcements.get_announcements()

        if not all_anns:
            st.info("No announcements available.")
        else:
            for ann in all_anns:
                st.markdown(f"### {ann['title']}")
                st.write(ann["message"])
                st.caption(f"Posted by {ann['author']} on {ann['timestamp']}")
                st.divider()

    # --- SUBMIT REQUESTS SECTION ---
    elif choice == "Submit Issue or Maintenance Request":
        st.header("Submit Issue or Maintenance Request")

        title = st.text_input("Request Title", key="issue_title_input")
        description = st.text_area("Request Description", key="issue_description_input")

        if st.button("Submit Request", key="submit_issue_button"):
            if not title or not description:
                st.error("Please enter both a title and description.")
            else:
                issues.create_issue(
                    title=title,
                    description=description,
                    created_by=st.session_state["user"]
                )
                st.success("Request submitted successfully!")
                st.rerun()

    # --- MY REQUESTS SECTION ---
    elif choice == "My Requests":
        st.header("Your Requests")

        # Dropdown filter
        filter_option = st.selectbox(
            "View:",
            ["Active", "Closed"],
            key="request_filter"
        )

        # Fetch all issues for this user
        user_issues = issues.get_issues_by_user(st.session_state["user"])

        if not user_issues:
            st.info("You have not submitted any requests yet.")
        else:
            # Filter logic
            if filter_option == "Active":
                filtered = [
                    issue for issue in user_issues
                    if issue["status"] in ["Submitted", "In Progress"]
                ]
            else:  # Closed
                filtered = [
                    issue for issue in user_issues
                    if issue["status"] == "Completed"
                ]

            # Display filtered results
            if not filtered:
                st.info(f"No {filter_option.lower()} requests.")
            else:
                for issue in filtered:
                    st.markdown(f"### {issue['title']}")
                    st.write(issue["description"])
                    st.caption(f"Status: {issue['status']}")
                    st.caption(f"Submitted: {issue['created_at']}")

                # NEW: Show last update timestamp if available
                if issue["history"]:
                    last_update = issue["history"][-1]["at"]
                    st.caption(f"Last Updated: {last_update}")
                    last_actor = issue["history"][-1]["updated_by"]
                    st.caption(f"Updated By: {last_actor}")
                st.divider()

# ---------------------------
# BOARD DASHBOARD
# ---------------------------
def board_dashboard():
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("HOA System")
    st.sidebar.write(f"Logged in as: **{st.session_state['user']}**")
    st.sidebar.write(f"Role: **{st.session_state['role']}**")

    menu = [
        "Home",
        "Announcements",
        "Post Announcement",
        "Pending Requests",
        "Documents",
        "Logout"
    ]
    choice = st.sidebar.radio("Navigation", menu)

    # --- PERSISTENT HEADER ---
    st.title("HOA Digital Management System")
    st.write("Initial prototype – Unit 4 implementation demo.")

    st.success(f"Welcome, {st.session_state['user']}!")
    st.write(f"Your role: **{st.session_state['role']}**")
    st.divider()

    # --- LOGOUT HANDLER ---
    if choice == "Logout":
        st.session_state.clear()
        st.rerun()

    # --- MODULE CONTENT ---

    # HOME
    if choice == "Home":
        st.subheader("Board Home")
        st.write("Use the sidebar to navigate board tools.")

    # ANNOUNCEMENTS VIEW
    elif choice == "Announcements":
        st.subheader("Community Announcements")
        all_anns = announcements.get_announcements()

        if not all_anns:
            st.info("No announcements available.")
        else:
            for ann in all_anns:
                st.markdown(f"### {ann['title']}")
                st.write(ann["message"])
                st.caption(f"Posted by {ann['author']} on {ann['timestamp']}")
                st.divider()

    # POST ANNOUNCEMENT
    elif choice == "Post Announcement":
        st.subheader("Create Announcement")

        title = st.text_input("Announcement Title")
        message = st.text_area("Announcement Message")

        if st.button("Post Announcement"):
            if title and message:
                announcements.add_announcement(
                    title,
                    message,
                    st.session_state["user"]
                )
                st.success("Announcement posted!")
                st.rerun()
            else:
                st.error("Please enter both a title and a message.")

    # PENDING REQUESTS
    elif choice == "Pending Requests":
        st.subheader("Pending Requests")

    # Show confirmation message after rerun
    if "status_message" in st.session_state:
        st.success(st.session_state["status_message"])
        del st.session_state["status_message"]

    # Status filter dropdown
        status_filter = st.selectbox(
            "Filter by status:",
            ["New", "In Process", "Complete"],
            key="board_request_filter"
        )

        # Map dropdown labels to actual status values
        status_map = {
            "New": "Submitted",
            "In Process": "In Progress",
            "Complete": "Completed"
        }

        selected_status = status_map[status_filter]

        # Fetch all issues
        all_issues = issues.get_all_issues()

        # Filter by selected status
        filtered = [i for i in all_issues if i["status"] == selected_status]

        if not filtered:
            st.info(f"No {status_filter.lower()} requests.")
        else:
            for issue in filtered:
                st.markdown(f"### {issue['title']}")
                st.write(issue["description"])
                st.caption(f"Submitted: {issue['created_at']}")

                # Show last update if available
                if issue["history"]:
                    last_update = issue["history"][-1]["at"]
                    last_actor = issue["history"][-1]["updated_by"]
                    st.caption(f"Last Updated: {last_update}")
                    st.caption(f"Updated By: {last_actor}")

                # Status update dropdown
                new_status = st.selectbox(
                    f"Update status for {issue['id']}",
                    ["Submitted", "In Progress", "Completed"],
                    index=["Submitted", "In Progress", "Completed"].index(issue["status"]),
                    key=f"status_{issue['id']}"
                )

                if st.button(f"Save Status {issue['id']}"):
                    issues.update_issue_status(
                        issue_id=issue['id'],
                        status=new_status,
                        actor=st.session_state["user"]
                    )
                    st.session_state["status_message"] = f"Status updated for {issue['id']}"
                    st.rerun()


                st.divider()

    # DOCUMENTS
    elif choice == "Documents":
        st.subheader("Document Repository")

        uploaded_file = st.file_uploader("Upload a new governing document")

        if uploaded_file:
            documents.upload_document(
                uploaded_file,
                uploaded_file.name,
                st.session_state["user"]
            )
            st.success("Document uploaded successfully!")
            st.rerun()

        # List existing documents
        doc_list = documents.list_documents()

        if not doc_list:
            st.info("No documents uploaded yet.")
        else:
            for doc in doc_list:
                st.markdown(f"### {doc['name']} (v{doc['version']})")
                st.caption(f"Uploaded by {doc['uploaded_by']} on {doc['timestamp']}")
                st.divider()


# ---------------------------
# ADMIN DASHBOARD
# ---------------------------
def admin_dashboard():
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("HOA System")
    st.sidebar.write(f"Logged in as: **{st.session_state['user']}**")
    st.sidebar.write(f"Role: **{st.session_state['role']}**")

    menu = [
        "Home",
        "User Management",
        "All Requests",
        "Documents",
        "Announcements",
        "Logout"
    ]
    choice = st.sidebar.radio("Navigation", menu)

    # --- PERSISTENT HEADER ---
    st.title("HOA Digital Management System")
    st.write("Initial prototype – Unit 4 implementation demo.")

    st.success(f"Welcome, {st.session_state['user']}!")
    st.write(f"Your role: **{st.session_state['role']}**")
    st.divider()

    # --- LOGOUT HANDLER ---
    if choice == "Logout":
        st.session_state.clear()
        st.rerun()

    # --- MODULE CONTENT ---

    # HOME
    if choice == "Home":
        st.subheader("Admin Home")
        st.write("Use the sidebar to manage users, requests, documents, and announcements.")

    # USER MANAGEMENT
    elif choice == "User Management":
        st.subheader("User Management")

        st.write("Create new users and assign roles.")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ["resident", "board", "admin"])

        if st.button("Create User"):
            try:
                auth.create_user(new_user, new_pass, new_role)
                st.success(f"User '{new_user}' created successfully.")
            except Exception as e:
                st.error(str(e))

        st.divider()

        st.subheader("Existing Users")
        users = auth.list_users()

        if not users:
            st.info("No users found.")
        else:
            for u in users:
                st.write(f"**{u['username']}** — Role: {u['role']}")
            st.divider()

    # ALL REQUESTS
    elif choice == "All Requests":
        st.subheader("All Requests")

        # Status filter dropdown
        status_filter = st.selectbox(
            "Filter by status:",
            ["New", "In Process", "Complete", "All"],
            key="admin_request_filter"
        )

        status_map = {
            "New": "Submitted",
            "In Process": "In Progress",
            "Complete": "Completed",
            "All": None
        }

        selected_status = status_map[status_filter]

        all_issues = issues.get_all_issues()

        if selected_status:
            filtered = [i for i in all_issues if i["status"] == selected_status]
        else:
            filtered = all_issues

        if not filtered:
            st.info(f"No {status_filter.lower()} requests.")
        else:
            for issue in filtered:
                st.markdown(f"### {issue['title']}")
                st.write(issue["description"])
                st.caption(f"Submitted: {issue['created_at']}")

                if issue["history"]:
                    last_update = issue["history"][-1]["at"]
                    last_actor = issue["history"][-1]["updated_by"]
                    st.caption(f"Last Updated: {last_update}")
                    st.caption(f"Updated By: {last_actor}")

                new_status = st.selectbox(
                    f"Update status for {issue['id']}",
                    ["Submitted", "In Progress", "Completed"],
                    index=["Submitted", "In Progress", "Completed"].index(issue["status"]),
                    key=f"admin_status_{issue['id']}"
                )

                if st.button(f"Save Status {issue['id']}"):
                    issues.update_issue_status(
                        issue_id=issue["id"],
                        status=new_status,
                        actor=st.session_state["user"]
                    )
                    st.session_state["status_message"] = f"Status updated for {issue['id']}"
                    st.rerun()

                st.divider()

        if "status_message" in st.session_state:
            st.success(st.session_state["status_message"])
            del st.session_state["status_message"]

    # DOCUMENTS
    elif choice == "Documents":
        st.subheader("Document Repository")

        uploaded_file = st.file_uploader("Upload a new governing document")

        if uploaded_file:
            documents.upload_document(
                uploaded_file.name,
                uploaded_file.read(),
                st.session_state["user"]
            )
            st.success("Document uploaded successfully!")
            st.rerun()

        doc_list = documents.list_documents()

        if not doc_list:
            st.info("No documents uploaded yet.")
        else:
            for doc in doc_list:
                st.markdown(f"### {doc['name']} (v{doc['version_id']})")
                st.caption(f"Uploaded by {doc['uploaded_by']} on {doc['timestamp']}")
                st.divider()

    # ANNOUNCEMENTS
    elif choice == "Announcements":
        st.subheader("Announcements")

        title = st.text_input("Announcement Title")
        message = st.text_area("Announcement Message")

        if st.button("Post Announcement"):
            announcements.add_announcement(
                title,
                message,
                st.session_state["user"]
            )
            st.success("Announcement posted!")
            st.rerun()

        st.divider()

        all_anns = announcements.get_announcements()

        if not all_anns:
            st.info("No announcements available.")
        else:
            for ann in all_anns:
                st.markdown(f"### {ann['title']}")
                st.write(ann["message"])
                st.caption(f"Posted by {ann['author']} on {ann['timestamp']}")
                st.divider()


# ---------------------------
# MAIN APP ROUTER
# ---------------------------
def main():
    if "user" not in st.session_state:
        login_screen()
        return

    role = st.session_state["role"]

    if role == "resident":
        resident_dashboard()
    elif role == "board":
        board_dashboard()
    elif role == "admin":
        admin_dashboard()
    else:
        st.error("Unknown role. Contact system administrator.")


if __name__ == "__main__":
    main()
