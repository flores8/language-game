import weave
import wandb
import os
from openai import OpenAI
import streamlit as st
import logging
from typing import Optional

wandb_key = os.environ.get("WANDB_KEY")
wandb.login(key=wandb_key)
weave.init("wandb-designers/language-translation-game")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

client: Optional[OpenAI] = None
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    st.error("Failed to initialize OpenAI client. Please check your API key.")

@weave.op()
def translate_text(text, target_language):
    if client is None:
        logger.error("OpenAI client is not initialized")
        return "Error: OpenAI client is not initialized. Please check your API key."
    
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
        logger.error(f"An error occurred during translation: {e}")
        return f"Error during translation: {str(e)}"

@weave.op()
def generate_sentence():
    if client is None:
        logger.error("OpenAI client is not initialized")
        return "Error: OpenAI client is not initialized. Please check your API key."
    
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
        logger.error(f"An error occurred during sentence generation: {e}")
        return f"Error during sentence generation: {str(e)}"
