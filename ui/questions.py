import streamlit as st
from services.repository import execute, fetch_all

def render_questions(role="USER"):
    st.header("Questions")

    # ============ ADMIN VIEW ============
    if role == "ADMIN":
        subs = fetch_all("SELECT id, name FROM sub_areas")

        # Initialize session state for form fields
        if "question_text" not in st.session_state:
            st.session_state.question_text = ""

        with st.form("add_question"):
            s = st.selectbox("Sub-Area", subs, format_func=lambda x: x[1])
            q = st.text_area("Question", value=st.session_state.question_text)
            if st.form_submit_button("Add Question"):
                # Validate and prevent duplicate question text
                if not q.strip():
                    st.error("Question cannot be empty.")
                else:
                    existing = fetch_all("SELECT id FROM questions WHERE question = ?", (q.strip(),))
                    if existing:
                        st.error("This question already exists.")
                    else:
                        execute(
                            "INSERT INTO questions (sub_area_id, question, option_type) VALUES (?, ?, 'SCALE_1_5')",
                            (s[0], q.strip())
                        )
                        # Clear fields after successful submission
                        st.session_state.question_text = ""
                        st.success("Question added")
                        st.rerun()

        st.divider()
        st.subheader("📋 Added Questions")
        
        questions_list = fetch_all("SELECT id, question FROM questions ORDER BY id")
        
        if questions_list:
            for index, (q_id, question_text) in enumerate(questions_list, 1):
                st.subheader(f"{index}. {question_text}")
                col1, col2 = st.columns([6, 1])
                
                with col1:
                    new_question = st.text_area(
                        "Question",
                        question_text,
                        key=f"qn{q_id}",
                        label_visibility="collapsed",
                        height=50
                    )
                    if new_question != question_text:
                        if not new_question.strip():
                            st.error("Question cannot be empty.")
                        else:
                            dup = fetch_all(
                                "SELECT id FROM questions WHERE question = ? AND id != ?",
                                (new_question.strip(), q_id)
                            )
                            if dup:
                                st.error("Another question with the same text exists.")
                            else:
                                execute(
                                    "UPDATE questions SET question=? WHERE id=?",
                                    (new_question.strip(), q_id)
                                )
                                st.rerun()
                
                with col2:
                    if st.button("🗑️", key=f"qd{q_id}", help="Delete"):
                        execute("DELETE FROM questions WHERE id=?", (q_id,))
                        st.rerun()
        else:
            st.info("No questions added yet.")

    # ============ ASSESSOR VIEW ============
    else:
        questions = fetch_all("SELECT id, question FROM questions")
        
        if not questions:
            st.info("No questions available yet.")
            return

        # Initialize session state for answers if needed
        if "assessor_answers" not in st.session_state:
            st.session_state.assessor_answers = {}

        # Define option labels for 5-point scale
        option_labels = {
            1: "Strongly Disagree",
            2: "Disagree",
            3: "Neutral",
            4: "Agree",
            5: "Strongly Agree"
        }

        # Display each question with radio buttons for single selection
        for q_id, q_text in questions:
            st.subheader(q_text)
            
            # Radio buttons for 5 options (single select only)
            answer = st.radio(
                "Select your response:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: option_labels[x],
                key=f"q_{q_id}",
                horizontal=False
            )
            
            # Store answer in session state
            st.session_state.assessor_answers[q_id] = answer
            st.divider()
        
        # Save answers button
        if st.button("Save Answers"):
            project_id = st.session_state.get("project_id")
            user_id = st.session_state.user.get("id")
            
            if not project_id:
                st.error("Please select a project first.")
                return
            
            if not user_id:
                st.error("User not found in session.")
                return
            
            try:
                for q_id, answer in st.session_state.assessor_answers.items():
                    # Delete existing answer if any
                    execute(
                        "DELETE FROM assessments WHERE question_id = ? AND project_id = ? AND user_id = ?",
                        (q_id, project_id, user_id)
                    )
                    # Insert new answer
                    execute(
                        "INSERT INTO assessments (question_id, project_id, user_id, response) VALUES (?, ?, ?, ?)",
                        (q_id, project_id, user_id, answer)
                    )
                st.success("Answers saved successfully!")
            except Exception as e:
                st.error(f"Failed to save answers: {str(e)}")
