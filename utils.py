import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

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

# Initialize OpenAI client
def get_openai_client():
    """Return an initialized OpenAI client"""
    api_key = load_api_key()
    if not api_key:
        st.error("OpenAI API key not found. Please set it in Streamlit secrets or .env file.")
        st.stop()
    return OpenAI(api_key=api_key) 