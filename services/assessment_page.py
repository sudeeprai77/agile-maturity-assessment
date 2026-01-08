import streamlit as st
from model.maturity_model import SUB_AREAS
from services.assessment_service import save_assessment

def render_assessment():
    project = st.text_input("Project Name")
    assessment_type = st.radio("Assessment Type", ["self", "evidence"])

    responses = []
    for area, subs in SUB_AREAS.items():
        st.subheader(area)
        for sub in subs:
            score = st.slider(sub, 1, 5, 3)
            responses.append((area, sub, score))

    if st.button("Save"):
        save_assessment(project, assessment_type, responses)
        st.success("Saved")
