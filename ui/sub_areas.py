import streamlit as st
from services.repository import execute, fetch_all

def render_sub_areas():
    st.header("Step 3: Sub-Areas")

    # Initialize session state for form fields
    if "subarea_name" not in st.session_state:
        st.session_state.subarea_name = ""
    if "subarea_weight" not in st.session_state:
        st.session_state.subarea_weight = 0

    areas = fetch_all("SELECT id, name FROM areas")

    with st.form("add_sub"):
        a = st.selectbox("Area", areas, format_func=lambda x: x[1])
        name = st.text_input("Sub-Area Name", value=st.session_state.subarea_name)
        weight = st.number_input("Weight (%)", 0, 100, value=st.session_state.subarea_weight)
        if st.form_submit_button("Add Sub-Area"):
            # Check for duplicate within same area
            existing = fetch_all(
                "SELECT id FROM sub_areas WHERE name = ? AND area_id = ?",
                (name, a[0])
            )
            if existing:
                st.error(f"Sub-area '{name}' already exists in this area.")
            elif not name.strip():
                st.error("Sub-area name cannot be empty.")
            else:
                execute(
                    "INSERT INTO sub_areas (area_id, name, weight) VALUES (?, ?, ?)",
                    (a[0], name, weight)
                )
                # Clear fields after successful submission
                st.session_state.subarea_name = ""
                st.session_state.subarea_weight = 0
                st.success("Added")
                st.rerun()

    st.divider()
    st.subheader("📋 Areas & Sub-Areas")

    # Fetch all areas to show mapping
    areas_list = fetch_all("SELECT id, name FROM areas ORDER BY id")

    if not areas_list:
        st.info("No areas available. Add areas first.")
        return

    for area_id, area_name in areas_list:
        with st.expander(f"📁 {area_name}"):
            subs = fetch_all(
                "SELECT id, name, weight FROM sub_areas WHERE area_id = ? ORDER BY id",
                (area_id,)
            )

            if not subs:
                st.write("No sub-areas for this area yet.")
                continue

            for index, (sa_id, name, weight) in enumerate(subs, 1):
                # Render sub-area on a single horizontal row: index | name (editable) | weight (editable) | delete
                col_idx, col_name, col_weight, col_del = st.columns([0.4, 6.0, 1.0, 0.6])

                with col_idx:
                    st.write(f"{index}.")

                with col_name:
                    new_name = st.text_input(
                        "Name",
                        name,
                        key=f"san{sa_id}",
                        label_visibility="collapsed"
                    )
                    if new_name != name:
                        if not new_name.strip():
                            st.error("Sub-area name cannot be empty.")
                        else:
                            dup = fetch_all(
                                "SELECT id FROM sub_areas WHERE name = ? AND area_id = ? AND id != ?",
                                (new_name.strip(), area_id, sa_id)
                            )
                            if dup:
                                st.error(f"Sub-area '{new_name}' already exists in this area.")
                            else:
                                execute(
                                    "UPDATE sub_areas SET name=? WHERE id=?",
                                    (new_name.strip(), sa_id)
                                )
                                st.rerun()

                with col_weight:
                    new_weight = st.number_input(
                        "Weight",
                        0,
                        100,
                        weight,
                        key=f"saw{sa_id}",
                        label_visibility="collapsed"
                    )
                    if new_weight != weight:
                        execute(
                            "UPDATE sub_areas SET weight=? WHERE id=?",
                            (new_weight, sa_id)
                        )
                        st.rerun()

                with col_del:
                    if st.button("🗑️", key=f"sad{sa_id}", help="Delete"):
                        execute("DELETE FROM sub_areas WHERE id=?", (sa_id,))
                        st.rerun()
