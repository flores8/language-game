import random
from api_handler import translate_text, generate_sentence

LANGUAGES = ["English", "Mandarin Chinese", "Spanish", "Arabic", "Hindi", "Russian", "Japanese", "French", "German", "Swahili"]

def get_random_language():
    return random.choice(LANGUAGES)

def generate_options(correct_language):
    options = random.sample(LANGUAGES, 4)
    if correct_language not in options:
        options[0] = correct_language
    random.shuffle(options)
    return options

def get_translation_and_options():
    original_sentence = generate_sentence()
    if original_sentence is None:
        return None, None, None, None
    target_language = get_random_language()
    translated_sentence = translate_text(original_sentence, target_language)
    if translated_sentence is None:
        return None, None, None, None
    options = generate_options(target_language)
    return original_sentence, translated_sentence, target_language, options

def new_round(game_state):
    original_sentence, translated_sentence, correct_language, options = get_translation_and_options()
    if original_sentence is None or translated_sentence is None:
        raise ValueError("Failed to generate new round")
    
    game_state['original_sentence'] = original_sentence
    game_state['translated_sentence'] = translated_sentence
    game_state['correct_language'] = correct_language
    game_state['options'] = options
    
    return game_state

def check_answer_and_update(game_state, selected_language):
    if selected_language == game_state['correct_language']:
        game_state['score'] += 1
    
    game_state['round'] += 1
    
    if game_state['round'] <= 10:
        return new_round(game_state)
    else:
        return game_state

def init_game_state():
    return {
        'round': 1,
        'score': 0,
        'original_sentence': '',
        'translated_sentence': '',
        'correct_language': '',
        'options': []
    }
