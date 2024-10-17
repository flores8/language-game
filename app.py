import streamlit as st
from game_logic import get_random_language, generate_options, check_answer

st.title("Language Translation Game")

if 'current_language' not in st.session_state:
    st.session_state.current_language = get_random_language()
    st.session_state.options = generate_options(st.session_state.current_language)
    st.session_state.score = 0
    st.session_state.round = 1

st.write(f"Round: {st.session_state.round}/10")
st.write(f"Score: {st.session_state.score}")

# TODO: Add translation display here

for option in st.session_state.options:
    if st.button(option):
        if check_answer(option, st.session_state.current_language):
            st.success("Correct!")
            st.session_state.score += 10
        else:
            st.error(f"Incorrect. The correct answer was {st.session_state.current_language}.")
        
        if st.session_state.round < 10:
            st.session_state.round += 1
            st.session_state.current_language = get_random_language()
            st.session_state.options = generate_options(st.session_state.current_language)
            st.experimental_rerun()
        else:
            st.write("Game Over!")
            st.write(f"Final Score: {st.session_state.score}")

if st.button("New Game"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()