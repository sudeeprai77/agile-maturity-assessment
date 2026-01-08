import streamlit as st
from services.repository import execute, fetch_all, fetch_one

def render_projects():
    st.header("📁 Projects")

    if st.session_state.user["role"] != "ADMIN":
        st.error("Admins only")
        return

    # Create project form
    with st.form("add_project"):
        name = st.text_input("Project Name")
        if st.form_submit_button("Create Project"):
            execute(
                "INSERT INTO projects (name, owner_id) VALUES (?, ?)",
                (name, st.session_state.user["id"])
            )
            st.success("Project created")
            st.rerun()

    st.divider()
    st.subheader("📋 Existing Projects & Assessor Assignment")

    projects = fetch_all("SELECT id, name FROM projects")
    
    if not projects:
        st.info("No projects yet.")
        return
    
    for project_id, project_name in projects:
        with st.expander(f"📁 {project_name}", expanded=False):
            st.write(f"**Project ID:** {project_id}")
            
            # Get all assessors
            all_assessors = fetch_all(
                "SELECT id, username FROM users WHERE role = 'ASSESSOR' ORDER BY username"
            )
            
            if not all_assessors:
                st.info("No assessors available.")
                continue
            
            # Get currently assigned assessors
            assigned = fetch_all(
                """SELECT u.id FROM users u
                   INNER JOIN assessor_projects ap ON u.id = ap.assessor_id
                   WHERE ap.project_id = ? AND u.role = 'ASSESSOR'""",
                (project_id,)
            )
            assigned_ids = [a[0] for a in assigned]
            
            # Multi-select for assessors
            selected_assessors = st.multiselect(
                "Assign Assessors",
                options=all_assessors,
                default=[a for a in all_assessors if a[0] in assigned_ids],
                format_func=lambda x: x[1],
                key=f"assign_assessors_{project_id}"
            )
            
            if st.button("Update Assignments", key=f"update_assessors_{project_id}"):
                # Remove assessors not in selection
                selected_ids = [a[0] for a in selected_assessors]
                for assessor_id in assigned_ids:
                    if assessor_id not in selected_ids:
                        execute(
                            "DELETE FROM assessor_projects WHERE project_id = ? AND assessor_id = ?",
                            (project_id, assessor_id)
                        )
                
                # Add new assessors
                for assessor_id in selected_ids:
                    if assessor_id not in assigned_ids:
                        try:
                            execute(
                                "INSERT INTO assessor_projects (assessor_id, project_id) VALUES (?, ?)",
                                (assessor_id, project_id)
                            )
                        except Exception:
                            pass  # Already assigned
                
                st.success("Assessor assignments updated")
                st.rerun()
            
            # Display current assignments
            st.write("**Currently Assigned Assessors:**")
            if assigned:
                current_assigned = fetch_all(
                    """SELECT u.username FROM users u
                       INNER JOIN assessor_projects ap ON u.id = ap.assessor_id
                       WHERE ap.project_id = ? AND u.role = 'ASSESSOR'
                       ORDER BY u.username""",
                    (project_id,)
                )
                for (assessor,) in current_assigned:
                    st.write(f"- {assessor}")
            else:
                st.write("None")
