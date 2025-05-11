import streamlit as st
from datetime import datetime

# Title
st.title("📝 Daily Class Log Formatter for WhatsApp")

# Initialize class list in session state
if "classes" not in st.session_state:
    st.session_state.classes = []

# Class Form
with st.form("class_form", clear_on_submit=True):
    st.subheader("Add a Class Entry")
    name = st.text_input("Class Name")
    time = st.text_input("Day/Time (e.g., Sat 9.15)")
    attendance = st.text_input("Attendance (e.g., 9/9)")
    covered = st.text_area("Covered Material")
    extra = st.text_input("Extra Notes (optional)")

    submitted = st.form_submit_button("➕ Add Class")
    if submitted:
        if all([name, time, attendance, covered]):
            st.session_state.classes.append({
                "name": name,
                "time": time,
                "attendance": attendance,
                "covered": covered,
                "extra": extra
            })
            st.success(f"✅ Added class: {name}")
        else:
            st.error("⚠️ Please fill in all required fields.")

# Display and format message
if st.session_state.classes:
    st.subheader("📋 Class Log Summary")
    today = datetime.now().strftime("%a, %d/%m/%Y")
    message = f"{today}\n"
    for i, c in enumerate(st.session_state.classes, 1):
        line = f"{i}. {c['name']} {c['time']}"
        if c['extra']:
            line += f" ({c['extra']})"
        line += f"\nAttendance: {c['attendance']}\nCovered: {c['covered']}\n\n"
        message += line

    # Display message for copying
    st.text_area("🟩 Formatted WhatsApp Message", value=message, height=300)

    st.info("To copy, manually select the text above, and use your phone's clipboard functionality.")
    
    if st.button("♻️ Clear All Classes"):
        st.session_state.classes = []
        st.experimental_rerun()
else:
    st.info("👈 Add your first class to begin.")
