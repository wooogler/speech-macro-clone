import streamlit as st
from utils import get_openai_client, get_selected_model

# Initialize OpenAI client
client = get_openai_client()

def get_suggestions(question, user_input, temperature):
    """
    Generate extended reply suggestions based on a question and short user input
    
    Args:
        question (str): The question or message from somebody
        user_input (str): Short user response to extend
        temperature (float): Controls randomness in generation
        
    Returns:
        list: List of suggested extended replies
    """
    # Construct the prompt
    prompt = f"""Q: Do you want to go to the movies? Input: no A: No thanks, I'm busy this afternoon. 
Q: How are you? Input: good A: I'm pretty good. How are you? 
Q: {question} Input: {user_input} A:"""
    
    suggestions = []
    
    # Get 4 suggestions by calling API 4 times
    for _ in range(4):
        try:
            response = client.chat.completions.create(
                model=get_selected_model(),
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=100,
                stop=["Q:", "\n\n"]  # Stop generation at new question or double newline
            )
            
            suggestion = response.choices[0].message.content.strip()
            suggestions.append(suggestion)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            suggestions.append("Error occurred during API call.")
    
    return suggestions

def submit_on_enter():
    """Handle Enter key press to submit form"""
    if 'extend_last_question' not in st.session_state:
        st.session_state.extend_last_question = ""
    if 'extend_last_input' not in st.session_state:
        st.session_state.extend_last_input = ""
    
    # If either input has changed, trigger submission
    if (st.session_state.extend_question != st.session_state.extend_last_question or
        st.session_state.extend_input != st.session_state.extend_last_input):
        st.session_state.extend_last_question = st.session_state.extend_question
        st.session_state.extend_last_input = st.session_state.extend_input
        st.session_state.extend_submit_trigger = True

def show_extend_reply_ui():
    """Display the Extend Reply UI and handle interactions"""
    st.header("Extend Reply")

    # Add sidebar with prompt template
    with st.sidebar:
        st.subheader("Prompt Template Used")
        st.code("""Q: Do you want to go to the movies? Input: no A: No thanks, I'm busy this afternoon. 
Q: How are you? Input: good A: I'm pretty good. How are you? 
Q: {question} Input: {user_input} A:""")
        
        st.write("This prompt instructs the AI to use few-shot learning to extend a short response into a more natural reply.")

    # Initialize session state for submit trigger
    if 'extend_submit_trigger' not in st.session_state:
        st.session_state.extend_submit_trigger = False
    
    # Default values for inputs
    default_question = "hey how is it going?"
    default_input = "okay"

    # Input fields for Extend Reply with placeholder only (no default values in the field)
    question = st.text_input("Somebody says:", 
                            placeholder=default_question, 
                            key="extend_question", 
                            on_change=submit_on_enter)
    
    user_input = st.text_input("User Input:", 
                              placeholder=default_input, 
                              key="extend_input", 
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
            key="extend_temp"
        )
    with col3:
        st.write("🤪")

    # Button or Enter key submission
    button_clicked = st.button("Get Suggestions", key="extend_suggestions_btn")
    
    # Check if form should be submitted (either by button or Enter key)
    submit_form = button_clicked or st.session_state.extend_submit_trigger
    
    # Reset trigger after checking
    if st.session_state.extend_submit_trigger:
        st.session_state.extend_submit_trigger = False
    
    # If no input is provided, use default values
    actual_question = question if question else default_question
    actual_input = user_input if user_input else default_input
    
    if submit_form:
        with st.spinner("Generating suggestions..."):
            suggestions = get_suggestions(actual_question, actual_input, temperature)
            
            # Display suggestions with numbering
            st.subheader("Here are some phrases you can use:")
            for i, suggestion in enumerate(suggestions, 1):
                st.info(f"{i}. {suggestion}") 