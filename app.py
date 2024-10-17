import streamlit as st
from game_logic import get_translation_and_options, check_answer

st.title("Language Translation Game")

if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'score': 0,
        'round': 1,
        'original_sentence': '',
        'translated_sentence': '',
        'correct_language': '',
        'options': []
    }

def new_round():
    original, translated, language, options = get_translation_and_options()
    st.session_state.game_state.update({
        'original_sentence': original,
        'translated_sentence': translated,
        'correct_language': language,
        'options': options
    })

if st.session_state.game_state['round'] == 1 and not st.session_state.game_state['translated_sentence']:
    new_round()

st.write(f"Round: {st.session_state.game_state['round']}/10")
st.write(f"Score: {st.session_state.game_state['score']}")

st.write("Translated sentence:")
st.write(st.session_state.game_state['translated_sentence'])

st.write("What language is this translated to?")

for option in st.session_state.game_state['options']:
    if st.button(option):
        if check_answer(option, st.session_state.game_state['correct_language']):
            st.success("Correct!")
            st.session_state.game_state['score'] += 10
        else:
            st.error(f"Incorrect. The correct answer was {st.session_state.game_state['correct_language']}.")
        
        st.write(f"Original sentence: {st.session_state.game_state['original_sentence']}")
        
        if st.session_state.game_state['round'] < 10:
            st.session_state.game_state['round'] += 1
            new_round()
            st.experimental_rerun()
        else:
            st.write("Game Over!")
            st.write(f"Final Score: {st.session_state.game_state['score']}")

if st.button("New Game"):
    st.session_state.game_state = {
        'score': 0,
        'round': 1,
        'original_sentence': '',
        'translated_sentence': '',
        'correct_language': '',
        'options': []
    }
    new_round()
    st.experimental_rerun()