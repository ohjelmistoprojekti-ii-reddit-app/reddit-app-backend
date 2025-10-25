import re
import langid
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize
import asyncio
import torch



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
            # combined = combined.lower() # change all texts into lowercase (Summary is also written in lowercase if this is done.)
            combined = re.sub(r'https?://\S+|www\.\S+', '', combined) # remove links
            processed.append(combined)
    
    return processed

def is_bot(text):
    clean_text = re.sub(r'[_*~`]', '', text)
    bot_text = re.compile(r'i am a bot')
    return bool(bot_text.search(clean_text))

def remove_links(text):
    return re.sub(r'https?://\S+', '', text).strip()

async def batch_translate(sentences, original_language, tokenizer, model):
    prompts = [f"translate {original_language} to English: {s}" for s in sentences]
    inputs = tokenizer(prompts, return_tensors="pt", padding=True, truncation=True)
    with torch.inference_mode():  # Disable gradient tracking for faster inference
        outputs = model.generate(**inputs, max_length=256)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)


async def translate_into_english(text, tokenizer, model):
    try:
        # Identifies the original language of the title
        language, confidence = langid.classify(text)
        if language == 'en':
            return text
        if language not in language_names:
            return "This language is so far unsupported"
        
        # Identifies the name of language based on language_names dictionary
        original_language = language_names[language]
        text_without_links = remove_links(text)
        sentences = sent_tokenize(text_without_links, language=language_names[language])

        translations = await batch_translate(sentences, original_language, tokenizer, model)
    
        return " ".join(translations)
    except:
        return f"Error during translation"
    

# Process and clean up topic labels. This version is without LLM.
def process_topic_label(raw_topics):
    # Remove words that contain numbers or are very similar to each other
    top_words = []
    for raw_word in raw_topics:
        if any(char.isdigit() for char in raw_word):
            continue

        is_similar = False
        for top_word in top_words:
            if raw_word.lower() in top_word.lower() or top_word.lower() in raw_word.lower():
                is_similar = True
                break

        if not is_similar:
            top_words.append(raw_word)

    # Only include the top 3 words in the topic label
    top_three = top_words[:3]
    topic_text = " ".join(top_three)
    return topic_text.title() # Capitalize the first letter of each word

def clean_text(text):
    text = re.sub(r'#+.*', '', text)  # remove markdown headers
    text = re.sub(r'https?://\S+', '', text)  # remove URLs
    text = re.sub(r'\([^)]*\)', '', text)  # remove parentheticals
    text = re.sub(r'[^a-zA-Z0-9.,!?\'\"\-\s]', '', text)  # remove emojis, junk
    text = re.sub(r'\s+', ' ', text)  # normalize whitespace
    return text.strip()

def smart_split(text, tokenizer, max_tokens):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current_chunk = [], []
    current_len = 0

    for sentence in sentences:
        tokens = tokenizer.encode(sentence, add_special_tokens=False)
        if current_len + len(tokens) <= max_tokens:
            current_chunk.append(sentence)
            current_len += len(tokens)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk).strip())
            current_chunk = [sentence]
            current_len = len(tokens)

    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())

    return chunks

def filter_factual_sentences(text):
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    # Filter out non-factual ones
    factual_sentences = [s for s in sentences if is_factual_sentence(s)]

    return " ".join(factual_sentences)

def is_factual_sentence(sentence):
    sentence = sentence.strip().lower()

    # Rule 1: Remove questions
    if sentence.endswith('?'):
        return False

    # Rule 2: Minimum word count
    if len(sentence.split()) < 8:
        return False

    # Rule 3: Opinion/slang keywords 
    opinion_keywords = [
        'i think', 'i hope', 'lol', 'lmao', 'omg', 'swear', 'crazy',
    'obviously', 'seriously', 'guys', 'like the movies', 'wtf',
    'dolla', 'dumb', 'they don\'t care', 'no proof', 'they figure they\'ll be dead',
    'just saying', 'idk', 'literally', 'basically', 'my opinion', 'sounds like',
    'that’s why', 'i feel like', 'imo', 'smh', 'bruh', 'fuck'
    ]
    
    for phrase in opinion_keywords:
        if phrase in sentence:
            return False

    # Rule 4: Remove sentences with multiple exclamation or question marks  
    if sentence.count("!") > 2 or sentence.count("?") > 2:
        return False

    return True