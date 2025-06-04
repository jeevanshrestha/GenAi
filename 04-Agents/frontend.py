import streamlit as st

from editor import Editor

# Set page config
st.set_page_config(
    page_title="Chat Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Apply custom styles for theme support
st.markdown("""
    <style>
    .chat-msg {
        background-color: var(--secondary-background-color);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .user-msg {
        background-color: #4a90e2;
        color: white;
    }
    .ai-msg {
        background-color: #2d2d2d;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title & header
st.title("🤖 Chat with AI Agent")
st.write("I am your project Helper. What do you want me to build today?")

# Display previous messages
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "ai"
    st.markdown(f"""
    <div class="chat-msg {role}-msg">
        <strong>{'You' if role == 'user' else 'AI'}:</strong> {msg['content']}
    </div>
    """, unsafe_allow_html=True)

# Input form
with st.form("chat_input", clear_on_submit=True):
    user_input = st.text_input("Enter your project request (e.g., Build a dark-themed Next.js blog):")

    submitted = st.form_submit_button("Send")

editor = Editor()

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    ai_reply = editor.chat(user_input)
    st.session_state.messages.append({"role": "ai", "content": ai_reply})
    st.rerun()
