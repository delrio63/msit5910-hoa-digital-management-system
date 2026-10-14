import streamlit as st
import announcements
import maintenance
from hoa_core import auth, documents, issues


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
            st.session_state["logged_in"] = True

            # Initialize module states safely
            announcements.init_state()
            maintenance.init_state()
            

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

    # Persistent flag initialization
    if "request_submitted" not in st.session_state:
        st.session_state.request_submitted = False


    menu = ["Home", 
            "Announcements", 
            "Submit Issue or Maintenance Request", 
            "My Requests",  
            "Logout"
    ]
    choice = st.sidebar.radio("Navigation", menu)

    # --- PERSISTENT HEADER ---
    st.title("HOA Digital Management System")
    st.write("Resident Portal")

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
                st.caption(f"Published by {ann['published_by']} on {ann['published_at']}")
                st.divider()

    # --- SUBMIT REQUESTS SECTION ---
    elif choice == "Submit Issue or Maintenance Request":
        st.header("Submit Issue or Maintenance Request")

        description = st.text_area("Describe the issue", key="maintenance_description_input")

        if st.button("Submit Request", key="submit_maintenance_button"):
            if not description:
                st.error("Please enter a description.")
            else:
                maintenance.submit_request(
                    resident=st.session_state["user"],
                    description=description
                )
                st.session_state.request_submitted = True
                st.rerun()

        # Persistent confirmation message        
        if st.session_state.request_submitted:
            st.success("Your request has been submitted!")
            st.session_state.request_submitted = False

    # --- MY REQUESTS SECTION ---
    elif choice == "My Requests":
        st.header("Your Maintenance Requests")

        # Dropdown filter
        filter_option = st.selectbox(
            "View:",
            ["Active", "Closed"],
            key="request_filter"
        )

        # Fetch all maintenance requests for this user
        user_requests = maintenance.get_requests_by_user(st.session_state["user"])

        if not user_requests:
            st.info("You have not submitted any requests yet.")
        else:
            # Filter logic
            if filter_option == "Active":
                filtered = [
                    req for req in user_requests
                    if req["status"] in ["Submitted", "In Progress"]
                ]
            else:  # Closed
                filtered = [
                    req for req in user_requests
                    if req["status"] == "Completed"
                ]

            # Display filtered results
            if not filtered:
                st.info(f"No {filter_option.lower()} requests.")
            else:
                for req in filtered:
                    st.markdown("### Maintenance Request")
                    st.write(req["description"])
                    st.caption(f"Status: {req['status']}")
                    st.caption(f"Submitted: {req['timestamp']}")
                    st.divider()


# ---------------------------
# BOARD DASHBOARD
# ---------------------------
def board_dashboard():
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("HOA System")
    st.sidebar.write(f"Logged in as: **{st.session_state['user']}**")
    st.sidebar.write(f"Role: **{st.session_state['role']}**")

    # --- INITIALIZE CONFIRMATION FLAG ---
    if "announcement_submitted" not in st.session_state:
        st.session_state.announcement_submitted = False

    menu = [
        "Home",
        "Announcements",
        "Submit Announcement Request",
        "Issues and Requests",
        "Documents",
        "Logout"
    ]
    choice = st.sidebar.radio("Navigation", menu)

    # --- PERSISTENT HEADER ---
    st.title("HOA Digital Management System")
    st.write("Board Portal")
    st.success(f"Welcome, {st.session_state['user']}!")
    st.write(f"Your role: **{st.session_state['role']}**")
    st.divider()

    # --- LOGOUT HANDLER ---
    if choice == "Logout":
        st.session_state.clear()
        st.rerun()


    # ---------------------------
    # HOME
    # ---------------------------
    if choice == "Home":
        st.subheader("Board Home")
        st.write("Use the sidebar to navigate board tools.")

    # ---------------------------
    # ANNOUNCEMENTS VIEW
    # ---------------------------
    elif choice == "Announcements":
        st.subheader("Community Announcements (Published)")
        published = announcements.get_published()

        if not published:
            st.info("No published announcements available.")
        else:
            for ann in published:
                st.markdown(f"### {ann['title']}")
                st.write(ann['message'])
                st.caption(f"Published by {ann['published_by']} on {ann['published_at']}")
                st.divider()

                # Board-specific pending submissions
        st.subheader("Your Pending Submissions")
        pending = announcements.get_pending()
        user = st.session_state["user"]

        user_pending = [p for p in pending if p["author"] == user]

        if not user_pending:
            st.info("You have no pending announcements awaiting admin review.")
        else:
            for ann in user_pending:
                st.markdown(f"### {ann['title']}")
                st.write(ann["message"])
                st.caption(f"Submitted at: {ann['submitted_at']}")
                st.divider()

    # ---------------------------
    # SUBMIT ANNOUNCEMENT REQUEST
    # ---------------------------

    elif choice == "Submit Announcement Request":
        st.subheader("Submit Announcement for Admin Review")

        title = st.text_input("Announcement Title")
        message = st.text_area("Announcement Message")

        # Submit button
        if st.button("Submit Announcement Request"):
            if title and message:
                announcements.submit_announcement(
                    title=title,
                    message=message,
                    author=st.session_state["user"]
                )
                st.session_state.announcement_submitted = True
                st.rerun()
            else:
                st.error("Please enter both a title and a message.")

        # Persistent confirmation message AFTER rerun
        if st.session_state.announcement_submitted:
            st.success("Your announcement request has been submitted!")
            st.session_state.announcement_submitted = False


    # ---------------------------
    # ISSUES AND REQUESTS (Maintenance Requests)
    # ---------------------------
    elif choice == "Issues and Requests":
        st.subheader("Issues and Requests")

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

        # Fetch all maintenance requests
        all_requests = maintenance.get_requests()

        # Filter by selected status
        filtered = [req for req in all_requests if req["status"] == selected_status]

        if not filtered:
            st.info(f"No {status_filter.lower()} requests.")
        else:
            for index, req in enumerate(filtered):
                st.markdown("### Maintenance Request")
                st.write(req["description"])
                st.caption(f"Submitted by: {req['resident']}")
                st.caption(f"Submitted: {req['timestamp']}")
                st.caption(f"Current Status: {req['status']}")

                # Status update dropdown
                new_status = st.selectbox(
                    f"Update status for request {index + 1}",
                    ["Submitted", "In Progress", "Completed"],
                    index=["Submitted", "In Progress", "Completed"].index(req["status"]),
                    key=f"status_{index}"
                )

                if st.button(f"Save Status {index + 1}", key=f"save_status_{index}"):
                    maintenance.update_status(index, new_status)
                    st.session_state["status_message"] = f"Status updated for request {index + 1}"
                    st.rerun()

                st.divider()

    # ---------------------------
    # DOCUMENTS
    # ---------------------------
    elif choice == "Documents":
        st.subheader("Document Repository")

        uploaded_file = st.file_uploader("Upload a new governing document", key="board_doc_upload")

        if uploaded_file and "board_pending_doc" not in st.session_state:
            st.session_state.board_pending_doc = uploaded_file
            st.info("File ready to save. Click 'Save Document' to store it permanently.")

        if "board_pending_doc" in st.session_state:
            if st.button("Save Document"):
                documents.upload_document(
                    st.session_state.board_pending_doc,
                    st.session_state.board_pending_doc.name,
                    st.session_state["user"]
                )
                st.success("Document uploaded successfully!")
                
                if "board_pending_doc" in st.session_state:
                    del st.session_state.board_pending_doc

                st.session_state.pop("board_doc_upload", None)

        doc_list = documents.list_documents()

        if not doc_list:
            st.info("No documents uploaded yet.")
        else:
            for doc in doc_list:
                st.markdown(f"### {doc['name']} (v{doc['version']})")
                st.caption(f"Uploaded by {doc['uploaded_by']} on {doc['uploaded_at']}")
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
    st.write("Admin Portal")
    st.success(f"Welcome, {st.session_state['user']}!")
    st.write(f"Your role: **{st.session_state['role']}**")
    st.divider()

    # ---------------------------
    # HOME
    # ---------------------------
    if choice == "Home":
        st.subheader("Admin Home")
        st.write("Use the sidebar to manage users, requests, documents, and announcements.")

    # ---------------------------
    # USER MANAGEMENT
    # ---------------------------
    elif choice == "User Management":
        st.subheader("User Management")

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

    # ---------------------------
    # ALL REQUESTS
    # ---------------------------
    elif choice == "All Requests":
        st.subheader("All Requests")

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

        filtered = (
            [i for i in all_issues if i["status"] == selected_status]
            if selected_status else all_issues
        )

        if not filtered:
            st.info(f"No {status_filter.lower()} requests.")
        else:
            for issue in filtered:
                st.markdown(f"### {issue['title']}")
                st.write(issue["description"])
                st.caption(f"publishedby: {issue['published_at']}")

                if issue.get("history"):
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

    # ---------------------------
    # DOCUMENTS
    # ---------------------------
    elif choice == "Documents":
        st.subheader("Document Repository")

        uploaded_file = st.file_uploader(
            "Upload a new governing document",
            key="board_doc_upload"
        )

        # Store file temporarily until user clicks Save
        if uploaded_file and "board_pending_doc" not in st.session_state:
            st.session_state.board_pending_doc = uploaded_file
            st.info("File ready to save. Click 'Save Document' to store it permanently.")

        # If a file is pending, show Save button
        if "board_pending_doc" in st.session_state:
            if st.button("Save Document"):
                documents.upload_document(
                    st.session_state.board_pending_doc,
                    st.session_state.board_pending_doc.name,
                    st.session_state["user"]
                )
                st.success("Document uploaded successfully!")

                # SAFE CLEANUP
                if "board_pending_doc" in st.session_state:
                    del st.session_state.board_pending_doc

                st.session_state.pop("board_doc_upload", None)
                st.rerun()

        # Display documents
        doc_list = documents.list_documents()

        if not doc_list:
            st.info("No documents uploaded yet.")
        else:
            for doc in doc_list:
                st.markdown(f"### {doc['name']} (v{doc['version']})")
                st.caption(f"Uploaded by {doc['uploaded_by']} on {doc['uploaded_at']}")
                st.divider()
                
    # ---------------------------
    # ANNOUNCEMENTS
    # ---------------------------
   
    elif choice == "Announcements":
        st.title("Announcement Management")
        
        # Show Replace-All success message after rerun
        if st.session_state.get("replace_success"):
            st.success("All announcements replaced.")
            st.session_state["replace_success"] = False

        # Reload pending announcements only when needed
        if st.session_state.get("reload_pending", False):
            st.subheader("Pending Announcements (Admin Edited)")
            pending = announcements.get_pending()
            st.session_state["reload_pending"] = False
        else:
            st.subheader("Pending Announcements (Board Submissions)")
            pending = announcements.get_pending()

        # ---------------------------
        # Pending announcements list
        # ---------------------------
        if not pending:
            st.info("No pending announcements.")
        else:
            for ann in pending:
                 # Refresh this announcement from the latest JSON
                refreshed = announcements.get_pending()[pending.index(ann)]
                ann = refreshed

                st.markdown(f"### {ann['title']}")
                st.write(ann["message"])

                if ann.get("edited"):
                    st.caption(f"Edited by {ann['edited_by']} on {ann['edited_at']}")
                else:
                    st.caption(f"Submitted by {ann['author']} on {ann['submitted_at']}")

                col1, col2, col3, col4 = st.columns(4)

                # Edit Mode toggle
                if col2.button(f"Edit", key=f"edit_{ann['id']}"):
                    st.session_state[f"edit_mode_{ann['id']}"] = True

                # Show edit fields when in edit mode
                if st.session_state.get(f"edit_mode_{ann['id']}", False):

                    new_title = st.text_input("Edit Title", value=ann["title"], key=f"title_{ann['id']}")
                    new_message = st.text_area("Edit Message", value=ann["message"], key=f"msg_{ann['id']}")

                    # Save Edits
                    if col1.button(f"Save Edits", key=f"save_{ann['id']}"):
                        announcements.edit_pending(
                            ann_id=ann["id"],
                            new_title=new_title,
                            new_message=new_message,
                            editor=st.session_state["user"]
                        )
                        # Refresh session_state with updated JSON
                        st.session_state.announcements_data = announcements._load_data()


                        st.session_state[f"saved_edits_{ann['id']}"] = True
                        st.success("Pending announcement updated.")
                        st.session_state["reload_pending"] = True
                        st.session_state[f"edit_mode_{ann['id']}"] = False
                        st.rerun()

                # Publish
                if col3.button(f"Publish", key=f"pub_{ann['id']}"):
                    if not st.session_state.get(f"saved_edits_{ann['id']}", False):
                        st.error("Publish not complete. Edits not saved. Click 'Save Edits' first.")
                    else:
                        announcements.publish_pending(ann["id"], editor=st.session_state["user"])
                        st.success("Announcement published.")
                        st.rerun()

                # Delete Pending
                if col4.button(f"Delete Pending", key=f"del_pending_{ann['id']}"):
                    announcements.delete_pending(ann["id"])
                    st.warning("Pending announcement deleted.")
                    st.session_state["reload_pending"] = True
                    st.rerun()

                st.divider()


        # ---------------------------
        # Add new announcement
        # ---------------------------
        st.subheader("Add New Announcement (Append Mode)")
        new_title = st.text_input("Title", key="new_title")
        new_message = st.text_area("Message", key="new_message")

        if st.button("Add Announcement"):
            if new_title and new_message:
                announcements.add_announcement(
                    title=new_title,
                    message=new_message,
                    author=st.session_state["user"]
                )
                st.success("Announcement added.")
                st.session_state["reload_pending"] = True
                st.rerun()
            else:
                st.error("Please enter both a title and a message.")

        st.divider()

        # ---------------------------
        # Replace ALL announcements
        # ---------------------------
        st.subheader("Replace ALL Published Announcements")
        rep_title = st.text_input("Replacement Title", key="rep_title")
        rep_message = st.text_area("Replacement Message", key="rep_message")

        if st.button("Replace All Announcements"):
            if rep_title and rep_message:
                announcements.replace_announcements(
                    title=rep_title,
                    message=rep_message,
                    author=st.session_state["user"]
                )
                st.success("All announcements replaced.")
                st.session_state["reload_pending"] = True
                st.session_state["replace_success"] = True
                st.rerun()
            else:
                st.error("Please enter both a title and a message.")

        st.divider()

        # ---------------------------
        # Published announcements
        # ---------------------------
        st.subheader("Published Announcements")
        published = announcements.get_published()

        if not published:
            st.info("No published announcements.")
        else:
            for ann in published:
                st.markdown(f"### {ann['title']}")
                st.write(ann["message"])
                st.caption(f"Published by {ann['published_by']} on {ann['published_at']}")

                if st.button(f"Delete Published", key=f"del_pub_{ann['id']}"):
                    announcements.delete_published(ann["id"])
                    st.warning("Published announcement deleted.")
                    st.rerun()

                st.divider()

# ---------------------------
# LOGOUT 
# ---------------------------
    elif choice == "Logout":
        st.session_state.clear()
        st.rerun()
    
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
