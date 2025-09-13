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