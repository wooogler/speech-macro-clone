import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Available models
AVAILABLE_MODELS = ["gpt-4o-mini", "gpt-3.5-turbo", "babbage-002"]

# Force reload of environment variables
def load_api_key():
    """Load and return the OpenAI API key from environment variables or Streamlit secrets"""
    # First try to get API key from Streamlit secrets (for Streamlit Cloud)
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        # If not found in secrets, try environment variables (for local development)
        load_dotenv(override=True)
        return os.getenv("OPENAI_API_KEY")

# Get selected model from session state or default
def get_selected_model():
    """Get the selected model from session state or default to gpt-4o-mini"""
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "gpt-4o-mini"
    return st.session_state.selected_model

# Show model selection in sidebar
def show_model_selection():
    """Display model selection in the sidebar"""
    with st.sidebar:
        st.subheader("Model Selection")
        selected_model = st.selectbox(
            "Select Model:",
            AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(get_selected_model()),
            key="model_selector"
        )
        st.session_state.selected_model = selected_model
        st.write(f"Current model: **{selected_model}**")

# Initialize OpenAI client
def get_openai_client():
    """Return an initialized OpenAI client"""
    api_key = load_api_key()
    if not api_key:
        st.error("OpenAI API key not found. Please set it in Streamlit secrets or .env file.")
        st.stop()
    return OpenAI(api_key=api_key) 