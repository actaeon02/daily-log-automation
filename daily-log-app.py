import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# Title
st.title("📝 Daily Class Log Formatter for WhatsApp")

# Initialize class list in session state
if "classes" not in st.session_state:
    st.session_state.classes = []

# Class Form
with st.form("class_form", clear_on_submit=True):
    st.subheader("Add a Class Entry")
    # Class to time options mapping
    class_time_map = {
        "SS2": ["TTh 13.30", "Sat 09.15"],
        "SS3": ["MW 13.30"],
        "SS4": ["MW 15.10", "TTh 16.40"],
        "HFD": ["TTh 15.10", "TTh 18.30"],
        "TB1": ["MW 16.40"],
        "TB6": ["WF 16.40"]
    }

    class_options = list(class_time_map.keys())

    # Let user pick class
    name = st.selectbox("Class Name", options=class_options, key="class_select")

    # Filter time options based on selected class
    filtered_times = class_time_map.get(name, [])

    # Let user pick time from filtered list
    time = st.selectbox("Day/Time", options=filtered_times, key="time_select")

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
    today = datetime.now().strftime("%d/%m/%Y")
    message = f"Jo, {today}\n"
    for i, c in enumerate(st.session_state.classes, 1):
        line = f"{i}. {c['name']} {c['time']}"
        if c['extra']:
            line += f" ({c['extra']})"
        line += f"\nAttendance: {c['attendance']}\nCovered: {c['covered']}\n\n"
        message += line

    # Display formatted message
    st.text_area("🟩 Formatted WhatsApp Message", value=message, height=300)

    # Styled HTML & JavaScript for the copy-to-clipboard button with a copyable icon
    copy_code = f"""
    <style>
        body {{
            margin: 0;
            padding: 0;
        }}
        .copy-btn {{
            background-color: #131720; /* Dark Background */
            color: white; /* White text */
            padding: 10px 12px; /* Padding */
            font-size: 15px; /* Font size */
            border: 1px solid #414149; /* Border */
            border-radius: 5px; /* Rounded corners */
            cursor: pointer; /* Pointer cursor on hover */
            text-align: center; /* Center text */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Shadow effect */
            transition: color 0.3s, border-color 0.3s; /* Smooth transition for color and border */
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: auto; /* Set width to auto to adjust the button size */
        }}
        
        .copy-btn:hover {{
            color: #c93e40; /* Change text color on hover */
            border-color: #c93e40; /* Change border color on hover */
        }}

        .copy-btn i {{
            margin-right: 10px; /* Space between icon and text */
            font-size: 15px; /* Icon size */
        }}
    </style>
    
    <script type="text/javascript">
    function copyToClipboard() {{
        var text = `{message}`;
        navigator.clipboard.writeText(text).then(function() {{
            alert("Message copied to clipboard!");
        }}, function(err) {{
            alert("Failed to copy text: ", err);
        }});
    }}
    </script>
    
    <button class="copy-btn" onclick="copyToClipboard()">
        📋 Copy to Clipboard
    </button>
    """

    # Render the HTML and JavaScript code using Streamlit's custom component
    components.html(copy_code, height=45)

    st.info("Tap the button above to copy the log.")

    # Clear all button
    if st.button("♻️ Clear All Classes"):
        st.session_state.classes = []
        st.experimental_rerun()
else:
    st.info("👈 Add your first class to begin.")
