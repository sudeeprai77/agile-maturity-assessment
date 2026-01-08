import streamlit as st
from services.repository import execute, fetch_all

def render_self_assessment():
    st.header("Step 5: Self Assessment")

    with st.form("create_assessment"):
        name = st.text_input("Assessment Name")
        by = st.text_input("Assessed By")
        if st.form_submit_button("Start"):
            execute(
    """
    INSERT INTO assessments (project_id, name, assessed_by, assessment_date)
    VALUES (?, ?, ?, date('now'))
    """,
    (st.session_state.project_id, name, st.session_state.user["id"])
)


    assessments = fetch_all("SELECT id, name FROM assessments")
    if not assessments:
        return

    a = st.selectbox("Assessment", assessments, format_func=lambda x: x[1])
    questions = fetch_all("SELECT id, question FROM questions")

    for qid, text in questions:
        lvl = st.radio(text, [1,2,3,4,5], key=f"a{a[0]}q{qid}")
        if st.button("Save", key=f"s{qid}"):
            execute(
                "INSERT INTO assessment_answers (assessment_id, question_id, selected_level) VALUES (?, ?, ?)",
                (a[0], qid, lvl)
            )
