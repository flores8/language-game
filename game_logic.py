import random
from api_handler import translate_text, generate_sentence

LANGUAGES = ["English", "Mandarin Chinese", "Spanish", "Arabic", "Hindi", "Russian", "Japanese", "French", "German", "Swahili"]

def get_random_language():
    return random.choice(LANGUAGES)

def generate_options(correct_language):
    options = random.sample(LANGUAGES, 3)
    if correct_language not in options:
        options[0] = correct_language
    random.shuffle(options)
    return options

def check_answer(user_choice, correct_language):
    return user_choice == correct_language

def get_translation_and_options():
    original_sentence = generate_sentence()
    target_language = get_random_language()
    translated_sentence = translate_text(original_sentence, target_language)
    options = generate_options(target_language)
    return original_sentence, translated_sentence, target_language, options