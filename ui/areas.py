import streamlit as st
from services.repository import execute, fetch_all

def render_areas():
    st.header("Step 2: Areas")

    # Initialize session state for form fields
    if "area_name" not in st.session_state:
        st.session_state.area_name = ""
    if "area_weight" not in st.session_state:
        st.session_state.area_weight = 0

    with st.form("add_area"):
        name = st.text_input("Area Name", value=st.session_state.area_name)
        weight = st.number_input("Weight (%)", 0, 100, value=st.session_state.area_weight)
        if st.form_submit_button("Add Area"):
            if not name.strip():
                st.error("Area name cannot be empty.")
            else:
                # Prevent duplicate area names
                existing = fetch_all("SELECT id FROM areas WHERE name = ?", (name.strip(),))
                if existing:
                    st.error(f"Area '{name}' already exists.")
                else:
                    try:
                        execute(
                            "INSERT INTO areas (name, weight) VALUES (?, ?)",
                            (name.strip(), weight)
                        )
                        # Clear fields after successful submission
                        st.session_state.area_name = ""
                        st.session_state.area_weight = 0
                        st.success("Area added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding area: {str(e)}")
    st.divider()
    st.subheader("📋 Added Areas")
    
    areas_list = fetch_all("SELECT id, name, weight FROM areas ORDER BY id")
    
    if areas_list:
        for index, (area_id, name, weight) in enumerate(areas_list, 1):
            st.subheader(f"{index}. {name}")
            col1, col2, col3 = st.columns([5.5, 0.5, 0.8])
            
            with col1:
                new_name = st.text_input(
                    "Name", 
                    name, 
                    key=f"an{area_id}",
                    label_visibility="collapsed"
                )
                if new_name != name:
                    # Prevent duplicate names when renaming
                    if not new_name.strip():
                        st.error("Area name cannot be empty.")
                    else:
                        dup = fetch_all(
                            "SELECT id FROM areas WHERE name = ? AND id != ?",
                            (new_name.strip(), area_id)
                        )
                        if dup:
                            st.error(f"Area '{new_name}' already exists.")
                        else:
                            execute(
                                "UPDATE areas SET name=? WHERE id=?",
                                (new_name.strip(), area_id)
                            )
                            st.rerun()
            
            with col2:
                new_weight = st.number_input(
                    "Weight", 
                    0, 
                    100, 
                    weight, 
                    key=f"aw{area_id}",
                    label_visibility="collapsed"
                )
                if new_weight != weight:
                    execute(
                        "UPDATE areas SET weight=? WHERE id=?",
                        (new_weight, area_id)
                    )
                    st.rerun()
            
            with col3:
                if st.button("🗑️", key=f"ad{area_id}", help="Delete"):
                    execute("DELETE FROM areas WHERE id=?", (area_id,))
                    st.rerun()
    else:
        st.info("No areas added yet.")