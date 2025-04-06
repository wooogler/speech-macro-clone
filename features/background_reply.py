import streamlit as st
from utils import get_openai_client, get_selected_model, get_model_type

# Initialize OpenAI client
client = get_openai_client()

def get_suggestions(question, background_info, temperature):
    """
    Generate reply suggestions incorporating user's background information
    
    Args:
        question (str): The question or message from somebody
        background_info (str): Background information about the user
        temperature (float): Controls randomness in generation
        
    Returns:
        list: List of suggested replies incorporating background info
    """
    # Construct the prompt
    prompt = f"""Consider this background information about myself: {background_info} 
Q: Where are you from? A: I am from Argentina, it is the southernest country of south america. 
Q: Do you have any hobbies? A: I love going on hikes and going horseback riding. 
Q: {question} 
A:"""
    
    suggestions = []
    model = get_selected_model()
    model_type = get_model_type(model)
    
    # Get 4 suggestions by calling API 4 times
    for _ in range(4):
        try:
            if model_type == "chat":
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    max_tokens=150,
                    stop=["Q:", "\n\n"]  # Stop generation at new question or double newline
                )
                suggestion = response.choices[0].message.content.strip()
            else:  # completion model
                response = client.completions.create(
                    model=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=150,
                    stop=["Q:", "\n\n"]  # Stop generation at new question or double newline
                )
                suggestion = response.choices[0].text.strip()
            
            suggestions.append(suggestion)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            suggestions.append("Error occurred during API call.")
    
    return suggestions

def submit_on_enter():
    """Handle Enter key press to submit form"""
    if 'bg_last_question' not in st.session_state:
        st.session_state.bg_last_question = ""
    if 'bg_last_info' not in st.session_state:
        st.session_state.bg_last_info = ""
    
    # If either input has changed, trigger submission
    if (st.session_state.background_question != st.session_state.bg_last_question or
        st.session_state.background_info_input != st.session_state.bg_last_info):
        st.session_state.bg_last_question = st.session_state.background_question
        st.session_state.bg_last_info = st.session_state.background_info_input
        st.session_state.bg_submit_trigger = True

def show_background_reply_ui():
    """Display the Reply with Background UI and handle interactions"""
    st.header("Reply with Background Information")

    # Add sidebar with prompt template
    with st.sidebar:
        st.subheader("Prompt Template Used")
        st.code("""Consider this background information about myself: {background_info} 
Q: Where are you from? A: I am from Argentina, it is the southernest country of south america. 
Q: Do you have any hobbies? A: I love going on hikes and going horseback riding. 
Q: {question} 
A:""")
        
        st.write("This prompt instructs the AI to incorporate your personal background information into its replies.")

    # Initialize session state for submit trigger
    if 'bg_submit_trigger' not in st.session_state:
        st.session_state.bg_submit_trigger = False
    
    # Default values for inputs
    default_question = "Do you like animals?"
    default_background = "I am from Argentina. I really like dancing, horseback-riding and being outdoors. I do not like insects. I love to eat ceviche, arepas, and tacos. I have a cat named Stella."

    # Input fields for Reply with Background with placeholder only (no default values in the field)
    question = st.text_input("Somebody says:", 
                            placeholder=default_question, 
                            key="background_question", 
                            on_change=submit_on_enter)
    
    background_info = st.text_area("Consider this info about me:", 
                                  placeholder=default_background, 
                                  height=100,
                                  key="background_info_input", 
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
            key="background_temp"
        )
    with col3:
        st.write("🤪")

    # Button or Enter key submission
    button_clicked = st.button("Get Suggestions", key="background_suggestions_btn")
    
    # Check if form should be submitted (either by button or Enter key)
    submit_form = button_clicked or st.session_state.bg_submit_trigger
    
    # Reset trigger after checking
    if st.session_state.bg_submit_trigger:
        st.session_state.bg_submit_trigger = False
    
    # If no input is provided, use default values
    actual_question = question if question else default_question
    actual_background = background_info if background_info else default_background
    
    if submit_form:
        with st.spinner("Generating suggestions..."):
            suggestions = get_suggestions(actual_question, actual_background, temperature)
            
            # Display suggestions with numbering
            st.subheader("Here are some phrases you can use:")
            for i, suggestion in enumerate(suggestions, 1):
                st.info(f"{i}. {suggestion}") 