def get_supported_languages():
    """
    Languages that Langid, Flan-t5 and NLTK support
    
    Sources:
    https://github.com/saffsd/langid.py
    https://dataloop.ai/library/model/google_flan-t5-large/
    https://github.com/nltk/nltk/issues/2055
    """
    language_names = {
        "cs": "Czech",
        "da": "Danish",
        "nl": "Dutch",
        "en": "English",
        "et": "Estonian",
        "fi": "Finnish",
        "fr": "French",
        "de": "German",
        "el": "Greek",
        "it": "Italian",
        "no": "Norwegian",
        "pl": "Polish",
        "pt": "Portuguese",
        "ru": "Russian",
        "sl": "Slovene",
        "es": "Spanish",
        "sv": "Swedish",
        "tr": "Turkish",
    }

    return language_names