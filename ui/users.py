import streamlit as st
from services.repository import execute, fetch_all, fetch_one
from services.auth import hash_password


def render_users():
    st.header("👤 User Management")

    # --------- ACCESS CONTROL ----------
    if st.session_state.user["role"] != "ADMIN":
        st.error("Only Admin users can manage users.")
        return

    # --------- ADD USER ----------
    with st.form("add_user_form"):
        st.subheader("➕ Create New User")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        role = st.selectbox(
            "Role",
            ["ADMIN", "ASSESSOR"],
            help="Admins can configure framework. Assessors can only do self assessments."
        )

        submitted = st.form_submit_button("Create User")

        if submitted:
            if not username or not password:
                st.error("Username and password are required.")
                return

            try:
                execute(
                    """
                    INSERT INTO users (username, password_hash, role)
                    VALUES (?, ?, ?)
                    """,
                    (username, hash_password(password), role)
                )
                st.success(f"User '{username}' created as {role}")
                st.rerun()
            except Exception as e:
                st.error("Username already exists.")

    st.divider()

    # --------- EXISTING USERS ----------
    st.subheader("📋 Existing Users & Project Mapping")

    users = fetch_all(
        "SELECT id, username, role FROM users ORDER BY role, username"
    )

    if not users:
        st.info("No users found.")
        return

    for uid, uname, role in users:
        with st.expander(f"👤 {uname} ({role})", expanded=False):
            st.write(f"**User ID:** {uid}")
            st.write(f"**Role:** {role}")
            
            if role == "ASSESSOR":
                # Show assigned projects for assessors
                assigned_projects = fetch_all(
                    """SELECT p.id, p.name FROM projects p
                       INNER JOIN assessor_projects ap ON p.id = ap.project_id
                       WHERE ap.assessor_id = ?
                       ORDER BY p.name""",
                    (uid,)
                )
                
                # Get all projects
                all_projects = fetch_all("SELECT id, name FROM projects ORDER BY name")
                
                if all_projects:
                    # Get assigned project IDs
                    assigned_ids = [p[0] for p in assigned_projects]
                    
                    # Multi-select for projects
                    selected_projects = st.multiselect(
                        "Assign Projects",
                        options=all_projects,
                        default=[p for p in all_projects if p[0] in assigned_ids],
                        format_func=lambda x: x[1],
                        key=f"assign_projects_{uid}"
                    )
                    
                    if st.button("Update Assignments", key=f"update_projects_{uid}"):
                        # Remove projects not in selection
                        selected_ids = [p[0] for p in selected_projects]
                        for project_id in assigned_ids:
                            if project_id not in selected_ids:
                                execute(
                                    "DELETE FROM assessor_projects WHERE assessor_id = ? AND project_id = ?",
                                    (uid, project_id)
                                )
                        
                        # Add new projects
                        for project_id in selected_ids:
                            if project_id not in assigned_ids:
                                try:
                                    execute(
                                        "INSERT INTO assessor_projects (assessor_id, project_id) VALUES (?, ?)",
                                        (uid, project_id)
                                    )
                                except Exception:
                                    pass  # Already assigned
                        
                        st.success("Project assignments updated")
                        st.rerun()
                    
                    # Display current assignments
                    st.write("**Currently Assigned Projects:**")
                    if assigned_projects:
                        for proj_id, proj_name in assigned_projects:
                            st.write(f"- {proj_name}")
                    else:
                        st.write("None")
                else:
                    st.info("No projects available. Create projects first.")
