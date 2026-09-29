import streamlit as st
from auth import login, logout
import rbac
import announcements
import maintenance

if "announcements" not in st.session_state:
    st.session_state.announcements = announcements.load_announcements()

st.set_page_config(page_title="HOA Digital Management System", page_icon="🏡")

st.title("HOA Digital Management System")
st.write("Initial prototype – Unit 4 implementation demo.")

# --- LOGIN SECTION ---
if "logged_in" not in st.session_state:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = login(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"Logged in as {username} ({role})")
            st.rerun()
        else:
            st.error("Invalid username or password")

else:
    # --- MAIN APP AFTER LOGIN ---
    st.success(f"Welcome, {st.session_state.username}!")
    st.write(f"Your role: **{st.session_state.role}**")

    # ============================
    # SIDEBAR NAVIGATION
    # ============================
    st.sidebar.title("HOA System")

    # Show logged-in user
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    st.sidebar.write(f"Role: **{st.session_state.role}**")

    # Navigation options based on role
    menu = []

    if st.session_state.role == "resident":
        menu = ["Home", "Announcements", "Submit Maintenance Request", "My Requests"]

    elif st.session_state.role in ["board_member", "admin"]:
        menu = ["Home", "Announcements", "Post Announcement", "Maintenance Dashboard"]

    menu.append("Logout")

    choice = st.sidebar.radio("Navigation", menu)

    # ============================
    # OLD ROLE-BASED CONTENT (COMMENTED OUT)
    # ============================
    # if rbac.can_view_board_dashboard(st.session_state.role):
    #     st.subheader("Board Dashboard")
    #     st.write("Board members and admins can see this section.")

    # if rbac.can_view_resident_portal(st.session_state.role):
    #     st.subheader("Resident Portal")
    #     st.write("Residents and admins can see this section.")

    # if rbac.is_admin(st.session_state.role):
    #     st.subheader("Admin Panel")
    #     st.write("Admins can manage system-wide settings here.")

    # ============================
    # MAIN CONTENT CONTROLLED BY choice
    # ============================

    if choice == "Home":
        st.subheader("Home")
        st.write("Use the sidebar to navigate.")

    elif choice == "Announcements":
        st.subheader("Community Announcements")
        for ann in announcements.get_announcements():
            st.markdown(f"### {ann['title']}")
            st.write(ann["message"])
            st.caption(f"Posted by {ann['author']} on {ann['timestamp']}")
            st.divider()

    elif choice == "Post Announcement" and rbac.is_admin(st.session_state.role):
        st.subheader("Create Announcement")
        title = st.text_input("Announcement Title")
        message = st.text_area("Announcement Message")

        if st.button("Post Announcement"):
            if title and message:
                announcements.add_announcement(title, message, st.session_state.username)
                st.success("Announcement posted!")
                st.rerun()
            else:
                st.error("Please enter both a title and a message.")

    elif choice == "Submit Maintenance Request":
        st.subheader("Submit Maintenance Request")
        description = st.text_area("Describe the issue")
        if st.button("Submit Request"):
            maintenance.submit_request(st.session_state.username, description)
            st.success("Request submitted!")

    elif choice == "My Requests":
        st.subheader("My Maintenance Requests")
        reqs = maintenance.get_requests()
        for r in reqs:
            if r["resident"] == st.session_state.username:
                st.write(f"**{r['description']}** — {r['status']} ({r['timestamp']})")

    elif choice == "Maintenance Dashboard":
        st.subheader("Maintenance Dashboard")
        reqs = maintenance.get_requests()
        for i, r in enumerate(reqs):
            st.write(f"**{r['resident']}** — {r['description']} ({r['timestamp']})")
            new_status = st.selectbox(
                f"Update status for request {i+1}",
                ["Submitted", "In Progress", "Completed"],
                index=["Submitted", "In Progress", "Completed"].index(r["status"]),
                key=f"status_{i}"
            )
            if st.button(f"Save Status {i+1}"):
                maintenance.update_status(i, new_status)
                st.success("Status updated!")
                st.rerun()

    elif choice == "Logout":
        st.session_state.clear()
        st.rerun()
