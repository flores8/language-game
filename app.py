import streamlit as st
from game_logic import get_translation_and_options, new_round, check_answer_and_update, init_game_state, is_language_match
from api_handler import client, log_guess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Guess the correct language!", page_icon="🌍", layout="wide")

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Guess the correct language!")

if 'game_state' not in st.session_state:
    st.session_state.game_state = init_game_state()

# Add this near the top of the file, after the imports
if client is None:
    st.error("Failed to initialize OpenAI client. Please check your API key.")
    st.stop()

def new_round_wrapper():
    logging.info("Starting new round")
    try:
        st.session_state.game_state = new_round(st.session_state.game_state)
        logging.info("Updated game state")
        return True
    except ValueError as e:
        st.error(str(e))
        logging.error(f"Error in new_round: {str(e)}")
        return False

if st.session_state.game_state['round'] == 1 and not st.session_state.game_state['original_sentence']:
    logging.info("Initializing first round")
    if not new_round_wrapper():
        st.stop()

if st.session_state.game_state['round'] <= 10:
    st.write(f"Round: {st.session_state.game_state['round']}/10")
    st.write(f"Score: {st.session_state.game_state['score']}")

    st.write(f"What language is this: {st.session_state.game_state['translated_sentence']}")

    st.markdown('<div class="language-buttons">', unsafe_allow_html=True)
    for i, option in enumerate(st.session_state.game_state['options']):
        if i % 2 == 0:
            cols = st.columns(2)
        if cols[i % 2].button(option, key=f"lang_{i}", use_container_width=True, type="primary"):
            previous_score = st.session_state.game_state['score']
            st.session_state.game_state = check_answer_and_update(st.session_state.game_state, option)
            
            # Determine if the answer was correct
            is_correct = st.session_state.game_state['score'] > previous_score
            
            # Log the guess to Weave
            log_guess(
                st.session_state.game_state['original_sentence'],
                st.session_state.game_state['translated_sentence'],
                st.session_state.game_state['correct_language'],
                option,
                is_correct
            )
            
            if is_correct:
                st.success(f"Correct! The language was {st.session_state.game_state['correct_language']}.")
            else:
                st.error(f"Sorry, that's incorrect. The correct language was {st.session_state.game_state['correct_language']}.")
            
            # Remove the time delay
            # time.sleep(1)  # This line should be removed
            
            if st.session_state.game_state['round'] <= 10:
                new_round_wrapper()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.write("Game Over!")
    st.write(f"Final Score: {st.session_state.game_state['score']}/10")

if st.button("Start a new game", key="NewGame", type="secondary"):
    st.session_state.game_state = init_game_state()
    new_round_wrapper()
    st.rerun()
