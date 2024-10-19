import os
from openai import OpenAI
import weave 
import streamlit as st

# Determine if we're running in a Streamlit Cloud environment
is_streamlit_cloud = os.environ.get('STREAMLIT_RUNTIME') == 'true'

if is_streamlit_cloud:
    # Use Streamlit secrets for production
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    # Use environment variable for local development
    api_key = os.getenv("OPENAI_API_KEY")

    # Optionally, you can add a check to ensure the API key is set
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

@weave.op()
def translate_text(text, target_language):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a translator. Translate the following text to {target_language}."},
                {"role": "user", "content": text}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

@weave.op()
def generate_sentence():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate a random sentence in English. The sentence should be between 6 to 12 words long."},
                {"role": "user", "content": "Generate a sentence."}
            ],
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred during sentence generation: {e}")
        return None

weave.init('language-translation-game')
