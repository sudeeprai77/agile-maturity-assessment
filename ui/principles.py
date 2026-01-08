import streamlit as st
from services.repository import execute, fetch_all

def render_principles():
    st.header("Step 1: Agile Principles")

    # Initialize session state for form fields
    if "principle_name" not in st.session_state:
        st.session_state.principle_name = ""
    if "principle_weight" not in st.session_state:
        st.session_state.principle_weight = 0

    with st.form("add_principle"):
        name = st.text_input("Principle Name", value=st.session_state.principle_name)
        weight = st.number_input("Weight (%)", 0, 100, value=st.session_state.principle_weight)
        if st.form_submit_button("Add Principle"):
            # Validate input and prevent duplicates
            if not name or not name.strip():
                st.error("Principle name cannot be empty.")
            else:
                nm = name.strip()
                existing = fetch_all("SELECT id FROM principles WHERE name = ?", (nm,))
                if existing:
                    st.error(f"Principle '{nm}' already exists.")
                else:
                    execute(
                        "INSERT INTO principles (name, weight) VALUES (?, ?)",
                        (nm, weight)
                    )
                    # Clear fields after successful submission
                    st.session_state.principle_name = ""
                    st.session_state.principle_weight = 0
                    st.success("Added")
                    st.rerun()

    st.divider()
    st.subheader("📋 Added Principles")
    
    principles_list = fetch_all("SELECT id, name, weight FROM principles ORDER BY id")
    
    if principles_list:
        for index, (pid, name, weight) in enumerate(principles_list, 1):
            st.subheader(f"{index}. {name}")
            col1, col2, col3 = st.columns([5.5, 0.5, 0.8])
            
            with col1:
                new_name = st.text_input(
                    "Name", 
                    name, 
                    key=f"pn{pid}",
                    label_visibility="collapsed"
                )
                if new_name != name:
                    if not new_name or not new_name.strip():
                        st.error("Principle name cannot be empty.")
                    else:
                        nm = new_name.strip()
                        dup = fetch_all(
                            "SELECT id FROM principles WHERE name = ? AND id != ?",
                            (nm, pid)
                        )
                        if dup:
                            st.error(f"Principle '{nm}' already exists.")
                        else:
                            execute(
                                "UPDATE principles SET name=? WHERE id=?",
                                (nm, pid)
                            )
                            st.rerun()
            
            with col2:
                new_weight = st.number_input(
                    "Weight", 
                    0, 
                    100, 
                    weight, 
                    key=f"pw{pid}",
                    label_visibility="collapsed"
                )
                if new_weight != weight:
                    execute(
                        "UPDATE principles SET weight=? WHERE id=?",
                        (new_weight, pid)
                    )
                    st.rerun()
            
            with col3:
                if st.button("🗑️", key=f"pd{pid}", help="Delete"):
                    execute("DELETE FROM principles WHERE id=?", (pid,))
                    st.rerun()
    else:
        st.info("No principles added yet.")
