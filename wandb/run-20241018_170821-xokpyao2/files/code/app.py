import streamlit as st
from game_logic import get_translation_and_options
import logging
import weave
from weave_app import game_panel, init_game_state, new_round, check_answer_and_update, GameState
import wandb

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize W&B
wandb.init(project="language-translation-game", entity="lauraleef")

st.set_page_config(page_title="Language Translation Game", page_icon="🌍", layout="wide")

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Language Translation Game")

if 'game_state' not in st.session_state:
    st.session_state.game_state = init_game_state()

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

if st.session_state.game_state.round == 1 and not st.session_state.game_state.original_sentence:
    logging.info("Initializing first round")
    if not new_round_wrapper():
        st.stop()

st.write(f"Round: {st.session_state.game_state.round}/10")
st.write(f"Score: {st.session_state.game_state.score}")

st.write("Translated sentence:")
st.write(st.session_state.game_state.translated_sentence)

st.write("What language is this translated to?")

st.markdown('<div class="language-buttons">', unsafe_allow_html=True)
for i, option in enumerate(st.session_state.game_state.options):
    if i % 2 == 0:
        cols = st.columns(2)
    if cols[i % 2].button(option, key=f"lang_{i}", use_container_width=True, type="primary"):
        st.session_state.game_state = check_answer_and_update(st.session_state.game_state, option)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.game_state.round > 10:
    st.write("Game Over!")
    st.write(f"Final Score: {st.session_state.game_state.score}")
    wandb.finish()

if st.button("New Game", key="NewGame"):
    wandb.finish()
    wandb.init(project="language-translation-game", entity="lauraleef")
    st.session_state.game_state = init_game_state()
    new_round_wrapper()
    st.rerun()

# Run the Weave app alongside Streamlit
weave.run(game_panel)
