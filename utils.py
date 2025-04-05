import os
from openai import OpenAI
from dotenv import load_dotenv

# Force reload of environment variables
def load_api_key():
    """Load and return the OpenAI API key from environment variables"""
    load_dotenv(override=True)
    return os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
def get_openai_client():
    """Return an initialized OpenAI client"""
    api_key = load_api_key()
    return OpenAI(api_key=api_key) 