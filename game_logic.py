import random

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