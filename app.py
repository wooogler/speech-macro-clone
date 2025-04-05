import streamlit as st
from features.extend_reply import show_extend_reply_ui
from features.background_reply import show_background_reply_ui
from features.keyword_request import show_keyword_request_ui

# Set page title and configuration
st.set_page_config(page_title="Speech Macro", page_icon="🎤")
st.title("Speech Macro")

# Create tabs for different features
tab1, tab2, tab3 = st.tabs(["Extend Reply", "Reply with Background", "Turn Words into Requests"])

# Show UI for each tab
with tab1:
    show_extend_reply_ui()

with tab2:
    show_background_reply_ui()
    
with tab3:
    show_keyword_request_ui() 