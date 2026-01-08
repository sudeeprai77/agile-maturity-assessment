import streamlit as st
from services.repository import fetch_all
from ui.principles import render_principles
from ui.areas import render_areas
from ui.sub_areas import render_sub_areas
from ui.questions import render_questions
from ui.self_assessment import render_self_assessment


def render_wizard():
    st.title("🧭 Agile Maturity Assessment Wizard")

    # ---------------- SESSION INIT ----------------
    if "wizard_step" not in st.session_state:
        st.session_state.wizard_step = 1

    if "project_id" not in st.session_state:
        st.session_state.project_id = None

    # ---------------- USER CHECK ----------------
    # Ensure we have a user in session and default role to non-admin
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

    # ---------------- ALLOWED STEPS (role-based) ----------------
    if role == "ADMIN":
        allowed_steps = [1, 2, 3, 4, 5]
    else:
        # Non-admins only see Questions (4) and Self Assessment (5)
        allowed_steps = [4, 5]

    # Ensure current wizard step is within allowed steps
    if st.session_state.wizard_step not in allowed_steps:
        st.session_state.wizard_step = allowed_steps[0]

    st.divider()

    # ---------------- WIZARD PROGRESS ----------------
    TOTAL_STEPS = len(allowed_steps)
    current_index = allowed_steps.index(st.session_state.wizard_step)
    st.progress((current_index + 1) / TOTAL_STEPS)

    # ---------------- STEP CONTENT ----------------
    if st.session_state.wizard_step == 1:
        st.header("Step 1: Agile Principles")

        if role == "ADMIN":
            render_principles()
        else:
            st.info("Only Admin users can configure Agile Principles.")

    elif st.session_state.wizard_step == 2:
        st.header("Step 2: Areas")

        if role == "ADMIN":
            render_areas()
        else:
            st.info("Only Admin users can configure Areas.")

    elif st.session_state.wizard_step == 3:
        st.header("Step 3: Sub-Areas")

        if role == "ADMIN":
            render_sub_areas()
        else:
            st.info("Only Admin users can configure Sub-Areas.")

    elif st.session_state.wizard_step == 4:
        if role == "ADMIN":
            st.header("Step 4: Questions")
        else:
            st.header("Questions")
            # Project selection for assessors
            st.subheader("📁 Project")
            user_id = user.get("id")
            projects = fetch_all(
                """SELECT p.id, p.name FROM projects p
                   INNER JOIN assessor_projects ap ON p.id = ap.project_id
                   WHERE ap.assessor_id = ?
                   ORDER BY p.name""",
                (user_id,)
            )
            if not projects:
                st.warning("No projects assigned to you. Contact admin.")
                st.stop()
            
            project = st.selectbox(
                "Select Project",
                projects,
                format_func=lambda x: x[1],
                key="project_selector_step4"
            )
            st.session_state.project_id = project[0]
            st.divider()

        # Both admins and non-admins should be able to view questions
        render_questions(role=role)

    elif st.session_state.wizard_step == 5:
        st.header("Step 5: Self Assessment")
        
        # Project selection for assessors
        if role != "ADMIN":
            st.subheader("📁 Project")
            user_id = user.get("id")
            projects = fetch_all(
                """SELECT p.id, p.name FROM projects p
                   INNER JOIN assessor_projects ap ON p.id = ap.project_id
                   WHERE ap.assessor_id = ?
                   ORDER BY p.name""",
                (user_id,)
            )
            if not projects:
                st.warning("No projects assigned to you. Contact admin.")
                st.stop()
            
            project = st.selectbox(
                "Select Project",
                projects,
                format_func=lambda x: x[1],
                key="project_selector_step5"
            )
            st.session_state.project_id = project[0]
            st.divider()

        # ✅ Everyone can access
        render_self_assessment()

    st.divider()

    # ---------------- NAVIGATION ----------------
    col1, col2, col3 = st.columns([1, 2, 1])

    def go_prev():
        idx = allowed_steps.index(st.session_state.wizard_step)
        if idx > 0:
            st.session_state.wizard_step = allowed_steps[idx - 1]

    def go_next():
        idx = allowed_steps.index(st.session_state.wizard_step)
        if idx < (len(allowed_steps) - 1):
            st.session_state.wizard_step = allowed_steps[idx + 1]

    with col1:
        if st.session_state.wizard_step != allowed_steps[0]:
            if st.button("⬅ Back"):
                go_prev()
                st.rerun()

    with col3:
        if st.session_state.wizard_step != allowed_steps[-1]:
            if st.button("Next ➡"):
                go_next()
                st.rerun()

