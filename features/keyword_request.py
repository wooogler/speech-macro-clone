import streamlit as st
from utils import get_openai_client

# Initialize OpenAI client
client = get_openai_client()

def get_suggestions(keyword, temperature):
    """
    Generate request phrase suggestions based on a simple keyword
    
    Args:
        keyword (str): The keyword to turn into a request
        temperature (float): Controls randomness in generation
        
    Returns:
        list: List of suggested request phrases
    """
    # Construct the prompt
    prompt = f"""Help: fruit Phrase: I'd like to have some fruit please 
Help: bed Phrase: Can you help me get to bed? 
Help: Shoes Phrase: can you help me put on these shoes? 
Help: {keyword} Phrase:"""
    
    suggestions = []
    
    # Get 4 suggestions by calling API 4 times
    for _ in range(4):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=50,
                stop=["Help:", "\n\n"]  # Stop generation at new help or double newline
            )
            
            suggestion = response.choices[0].message.content.strip()
            suggestions.append(suggestion)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            suggestions.append("Error occurred during API call.")
    
    return suggestions

def submit_on_enter():
    """Handle Enter key press to submit form"""
    if 'last_keyword' not in st.session_state:
        st.session_state.last_keyword = ""
    
    # If the keyword has changed, store it and set the trigger flag
    if st.session_state.keyword_input != st.session_state.last_keyword:
        st.session_state.last_keyword = st.session_state.keyword_input
        st.session_state.submit_trigger = True

def show_keyword_request_ui():
    """Display the Turn words into requests UI and handle interactions"""
    st.header("Turn Words into Requests")

    # Add sidebar with prompt template
    with st.sidebar:
        st.subheader("Prompt Template Used")
        st.code("""Help: fruit Phrase: I'd like to have some fruit please 
Help: bed Phrase: Can you help me get to bed? 
Help: Shoes Phrase: can you help me put on these shoes? 
Help: {keyword} Phrase:""")
        
        st.write("This prompt instructs the AI to convert a simple keyword into a natural request phrase.")

    # Initialize session state for submit trigger
    if 'submit_trigger' not in st.session_state:
        st.session_state.submit_trigger = False
    
    # Default value for keyword
    default_keyword = "pages"

    # Input field for keyword with placeholder only (no default value in the field)
    keyword = st.text_input("Keyword:", 
                           placeholder=default_keyword,
                           key="keyword_input", 
                           on_change=submit_on_enter)

    # Variability slider with emojis
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        st.write("🙂")
    with col2:
        temperature = st.slider(
            "Variability:",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.1,
            key="keyword_temp"
        )
    with col3:
        st.write("🤪")

    # Button or Enter key submission
    button_clicked = st.button("Get Suggestions", key="keyword_suggestions_btn")
    
    # Check if form should be submitted (either by button or Enter key)
    submit_form = button_clicked or st.session_state.submit_trigger
    
    # Reset trigger after checking
    if st.session_state.submit_trigger:
        st.session_state.submit_trigger = False
    
    # If no input is provided, use default value
    actual_keyword = keyword if keyword else default_keyword
    
    if submit_form:
        with st.spinner("Generating suggestions..."):
            suggestions = get_suggestions(actual_keyword, temperature)
            
            # Display suggestions with numbering
            st.subheader("Here are some phrases you can use:")
            for i, suggestion in enumerate(suggestions, 1):
                st.info(f"{i}. {suggestion}") 