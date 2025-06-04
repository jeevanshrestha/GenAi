import streamlit as st
import os
from dotenv import load_dotenv
from editor import Editor  # ← Your custom project generator

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Project Generator",
    page_icon="📁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize the Editor instance
@st.cache_resource
def initialize_editor():
    return Editor()

def main():
    st.title("📁 AI Project Generator")
    st.markdown("Chat with an AI to create GitHub-ready programming projects.")
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        st.info("You can get an API key from [OpenAI's website](https://platform.openai.com/api-keys)")
        return

    # Initialize Editor agent
    try:
        editor = initialize_editor()
    except Exception as e:
        st.error(f"Failed to initialize project assistant: {str(e)}")
        return

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Sidebar controls
    with st.sidebar:
        st.header("Project Controls")
        
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            editor.messages = []
            st.rerun()

        st.markdown("---")
        st.markdown("Ask me to build a starter project for any language or framework.")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Describe your project (e.g., Create a dark-themed React app)"):
        # User input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking ..."):
                try:
                    response = editor.chat(prompt)
                    if isinstance(response, dict):
                        content = "```json\n" + json.dumps(response, indent=2) + "\n```"
                    else:
                        content = response
                    st.markdown(content)
                    st.session_state.messages.append({"role": "assistant", "content": content})
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
