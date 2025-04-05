# Speech Macro

A Streamlit application that helps users generate natural language responses using OpenAI's GPT-3.5-turbo model.

## Features

- **Extend Reply**: Turn short responses into more natural, extended replies
- **Reply with Background Information**: Generate personalized responses based on your background
- **Turn Words into Requests**: Convert simple keywords into natural request phrases

## Implementation

This application is based on the research paper ["The less I type, the better": How AI Language Models can Enhance or Impede Communication for AAC Users](https://doi.org/10.1145/3544548.3581560) by Valencia et al. (2023). The paper explores how AI language models can enhance communication by reducing typing effort while maintaining user agency, which inspired the development of these features to help users craft more natural and personalized responses.

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   - Create a `.env` file in the root directory
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

Run the application:

```
streamlit run app.py
```

## Project Structure

- `app.py`: Main application file
- `features/`: Directory containing feature modules
  - `extend_reply.py`: Extend Reply feature
  - `background_reply.py`: Reply with Background Information feature
  - `keyword_request.py`: Turn Words into Requests feature
- `utils.py`: Utility functions
- `requirements.txt`: Project dependencies
