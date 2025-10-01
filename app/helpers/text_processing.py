import re
import langid
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

language_names = {
    "fi": "Finnish",
    "es": "Spanish",
    "it": "Italian",
    "sv": "Swedish"
    }


def is_english(text):
    try:
        language, confidence = langid.classify(text)
        return language == 'en'
    except:
        return False

def preprocess(posts):
    processed = []

    for post in posts:
        if is_english(post['title']):
            post_parts = [post['title'], post['content']]

            for comment in post['comments']:
                # leave out too short or non-English comments
                if comment and len(comment) > 10 and is_english(comment):
                    post_parts.append(comment)

            combined = " ".join(post_parts) # join a post into one string, separated by spaces
            combined = combined.lower() # change all texts into lowercase
            combined = re.sub(r'https?://\S+|www\.\S+', '', combined) # remove links
            processed.append(combined)
    
    return processed

def is_bot(text):
    clean_text = re.sub(r'[_*~`]', '', text)
    bot_text = re.compile(r'i am a bot')
    return bool(bot_text.search(clean_text))

def translator(comment):
    try:
        language, confidence = langid.classify(comment)
        if language not in language_names:
            return "Unsupported language"
        
        original_language = language_names[language]
        prompt = f"translate {original_language} to English: {comment}"
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        outputs = model.generate(input_ids, max_length=512)
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return translation
    except:
        return "Error during translation"
    