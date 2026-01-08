import streamlit as st
from ui.login import render_login
from ui.wizard import render_wizard
from ui.admin_dashboard import render_admin_dashboard
from services.auth import validate_session

st.set_page_config(page_title="Agile Maturity", layout="wide")

# Initialize session state defaults
if "user" not in st.session_state:
    st.session_state.user = None

if "session_token" not in st.session_state:
    st.session_state.session_token = None

if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1

if "project_id" not in st.session_state:
    st.session_state.project_id = None

if "admin_active_tab" not in st.session_state:
    st.session_state.admin_active_tab = "framework"

if "assessor_answers" not in st.session_state:
    st.session_state.assessor_answers = {}

# Check if user has a valid session token (persists across browser refresh)
if st.session_state.user is None and st.session_state.session_token:
    validated_user = validate_session(st.session_state.session_token)
    if validated_user:
        st.session_state.user = validated_user

# Check if user is authenticated
if st.session_state.user is None:
    render_login()
else:
    user = st.session_state.user
    if isinstance(user, dict):
        role = user.get("role", "USER").upper()
    else:
        role = getattr(user, "role", "USER")
        try:
            role = role.upper()
        except Exception:
            role = "USER"
    
    # Route based on role
    if role == "ADMIN":
        render_admin_dashboard()
    else:
        # Assessor view with logout button
        col_info, col_logout = st.columns([9, 1])
        with col_info:
            st.caption(f"Signed in: {user.get('id', 'unknown')} ({role})")
        with col_logout:
            if st.button("Log out"):
                from services.auth import logout_session
                if st.session_state.session_token:
                    logout_session(st.session_state.session_token)
                st.session_state.user = None
                st.session_state.session_token = None
                st.session_state.wizard_step = 1
                st.session_state.project_id = None
                st.session_state.assessor_answers = {}
                st.success("Logged out")
                st.rerun()
        
        render_wizard()
