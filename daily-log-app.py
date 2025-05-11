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

    # Display formatted message
    st.text_area("🟩 Formatted WhatsApp Message", value=message, height=300)

    # Styled HTML & JavaScript for the copy-to-clipboard button with a copyable icon
    copy_code = f"""
    <style>
        .copy-btn {{
            background-color: #131720; /* Dark Background */
            color: white; /* White text */
            padding: 6px 12px; /* Padding */
            font-size: 16px; /* Font size */
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
            margin-top: 10px; /* Reduce the gap between the button and the bottom elements */
            margin-bottom: 10px; /* Remove bottom margin */
        }}
        
        .copy-btn:hover {{
            color: #c93e40; /* Change text color on hover */
            border-color: #c93e40; /* Change border color on hover */
        }}

        .copy-btn i {{
            margin-right: 10px; /* Space between icon and text */
            font-size: 15px; /* Icon size */
        }}

        /* Reduce the overall margin/padding of the page content */
        .stButton {{
            margin-bottom: 10px !important; /* Override default button margin */
        }}

        /* Make sure there's no extra padding in the container of the button */
        .stTextArea {{
            margin-bottom: 10px !important; /* Reduce the space below the text area */
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
    components.html(copy_code)

    st.info("Tap the button above to copy the log to your clipboard.")

    # Clear all button
    if st.button("♻️ Clear All Classes"):
        st.session_state.classes = []
        st.experimental_rerun()
else:
    st.info("👈 Add your first class to begin.")
