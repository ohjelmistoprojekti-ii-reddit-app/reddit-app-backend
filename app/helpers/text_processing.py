import re
import langid


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

# Process and clean up topic labels. This version is without LLM or similar.
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

    top_three = top_words[:3]
    topic_text = " ".join(top_three)
    return topic_text.title()