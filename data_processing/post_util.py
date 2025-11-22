import asyncio
from data_processing.translation import translate_into_english
from transformers import T5Tokenizer, T5ForConditionalGeneration
import langid

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large", legacy=False)
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")

def is_valid_comment(comment):
    if not isinstance(comment, str):
        return False
    text = comment.strip()
    if len(text) < 10:
        return False
    return True


async def get_top_posts_with_translations(posts, n_posts=1):
    # Sort posts by Reddit score (upvotes - downvotes), descending
    top_posts = sorted(posts, key=lambda p: p["score"], reverse=True)[:n_posts]
    print(f"Translating posts..")
    
    for post in top_posts:
        text = post["title"] + " " + post["content"][:100]
        language, confidence = langid.classify(text)
        if language == 'en':
            post["comments_eng"] = []
            post["title_eng"] = ""
            post["content_eng"] = ""
            continue  # Skip translation for English posts
        
        post["comments_eng"] = []
        post["title_eng"] = await translate_into_english(post["title"], tokenizer, model)
        post["content_eng"] = await translate_into_english(post["content"], tokenizer, model)
        
        comment_tasks = [
            translate_into_english(comment, tokenizer, model)
            for comment in post["comments"]
            if is_valid_comment(comment)
        ]
        post["comments_eng"] = await asyncio.gather(*comment_tasks)

    return top_posts
