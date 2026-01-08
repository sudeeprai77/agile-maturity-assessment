import streamlit as st
from ui.users import render_users
from ui.projects import render_projects
from ui.wizard import render_wizard


def render_admin_dashboard():
    """Admin-only dashboard with navigation between Admin Controls and Wizard"""
    
    st.title("🔐 Admin Dashboard")
    
    # Check user is admin
    if "user" not in st.session_state or not st.session_state.user:
        st.warning("No user in session. Please log in.")
        return
    
    user = st.session_state.user
    if isinstance(user, dict):
        role = user.get("role", "USER").upper()
    else:
        role = getattr(user, "role", "USER")
        try:
            role = role.upper()
        except Exception:
            role = "USER"
    
    if role != "ADMIN":
        st.error("Only Admin users can access this dashboard.")
        return
    
    # User info and logout in top right
    col_info, col_logout = st.columns([9, 1])
    with col_info:
        st.caption(f"Signed in: {user.get('id', 'unknown')} ({role})")
    with col_logout:
        if st.button("Log out", key="logout_button"):
            from services.auth import logout_session
            if st.session_state.get("session_token"):
                logout_session(st.session_state.session_token)
            st.session_state.user = None
            st.session_state.session_token = None
            st.session_state.admin_active_tab = "framework"
            st.session_state.wizard_step = 1
            st.session_state.project_id = None
            st.success("Logged out")
            st.rerun()
    
    st.divider()
    
    # Initialize active tab in session state
    if "admin_active_tab" not in st.session_state:
        st.session_state.admin_active_tab = "framework"
    
    # Custom tab buttons that persist state
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Framework Setup", use_container_width=True, 
                     key="tab_framework",
                     type="primary" if st.session_state.admin_active_tab == "framework" else "secondary"):
            st.session_state.admin_active_tab = "framework"
    with col2:
        if st.button("📁 Project Management", use_container_width=True,
                     key="tab_projects",
                     type="primary" if st.session_state.admin_active_tab == "projects" else "secondary"):
            st.session_state.admin_active_tab = "projects"
    with col3:
        if st.button("👤 User Management", use_container_width=True,
                     key="tab_users",
                     type="primary" if st.session_state.admin_active_tab == "users" else "secondary"):
            st.session_state.admin_active_tab = "users"
    
    st.divider()
    
    # Display content based on active tab
    if st.session_state.admin_active_tab == "framework":
        st.subheader("📋 Framework Setup (Wizard)")
        render_wizard()
    elif st.session_state.admin_active_tab == "projects":
        st.subheader("📁 Project Management")
        render_projects()
    else:
        st.subheader("👤 User Management")
        render_users()
