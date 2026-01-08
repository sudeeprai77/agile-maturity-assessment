import streamlit as st
from services.auth import authenticate, create_session


def render_login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            # Create a persistent session token
            session_token = create_session(user["id"], user["username"], user["role"])
            if session_token:
                st.session_state.user = user
                st.session_state.session_token = session_token
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Failed to create session")
        else:
            st.error("Invalid username or password")
