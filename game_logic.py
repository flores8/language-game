import random
from api_handler import translate_text, generate_sentence

LANGUAGES = ["English", "Mandarin Chinese", "Spanish", "Arabic", "Hindi", "Russian", "Japanese", "French", "German", "Swahili"]

__all__ = ['get_translation_and_options', 'new_round', 'check_answer_and_update', 'init_game_state', 'is_language_match']

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
    translated_sentence, actual_language = translate_text(original_sentence, target_language)
    if translated_sentence is None or actual_language is None:
        return None, None, None, None
    
    options = generate_options(actual_language)
    return original_sentence, translated_sentence, actual_language, options

def is_similar(text1, text2):
    # Simple similarity check based on word count
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    common_words = words1.intersection(words2)
    similarity = len(common_words) / max(len(words1), len(words2))
    return similarity > 0.5  # Adjust this threshold as needed

def new_round(game_state):
    original_sentence, translated_sentence, correct_language, options = get_translation_and_options()
    if original_sentence is None or translated_sentence is None:
        raise ValueError("Failed to generate new round")
    
    game_state['original_sentence'] = original_sentence
    game_state['translated_sentence'] = translated_sentence
    game_state['correct_language'] = correct_language
    game_state['options'] = options
    
    return game_state

def is_language_match(selected, correct):
    selected = selected.lower()
    correct = correct.lower()
    
    # Direct match
    if selected == correct:
        return True
    
    # Partial match (e.g., "Chinese" matches "Mandarin Chinese")
    if selected in correct or correct in selected:
        return True
    
    # Special cases
    if (selected == "chinese" and correct == "mandarin chinese") or \
       (selected == "mandarin chinese" and correct == "chinese"):
        return True
    
    return False

def check_answer_and_update(game_state, selected_language):
    is_correct = is_language_match(selected_language, game_state['correct_language'])
    if is_correct:
        game_state['score'] += 1
    
    game_state['round'] += 1
    
    if game_state['round'] <= 10:
        game_state = new_round(game_state)
    
    return game_state, is_correct

def init_game_state():
    return {
        'round': 1,
        'score': 0,
        'original_sentence': '',
        'translated_sentence': '',
        'correct_language': '',
        'options': []
    }
