import asyncio
import langid
from app.helpers.text_processing import translate_into_english
from transformers import T5Tokenizer, T5ForConditionalGeneration
import datetime

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")


def is_valid_comment(comment):
    if not isinstance(comment, str):
        return False
    text = comment.strip()
    if len(text) < 5:
        return False
    return True


async def get_top_posts_with_translations(posts):
    # Sort posts by Reddit score (upvotes - downvotes), descending
    top_posts = sorted(posts, key=lambda p: p["score"], reverse=True)[:1]
    print("Translating posts into English..")

    for i, post in enumerate(top_posts):
        start = datetime.datetime.now()
        post["comments_eng"] = []
        post["title_eng"] = await translate_into_english(post["title"], tokenizer, model)
        post["content_eng"] = await translate_into_english(post["content"], tokenizer, model)
        
        comment_tasks = [
        translate_into_english(comment, tokenizer, model)
        for comment in post["comments"][:3]
        if is_valid_comment(comment)
        ]
        post["comments_eng"] = await asyncio.gather(*comment_tasks)
        end = datetime.datetime.now()
        print(f"Translated the post number {i+1} in {end - start}.")

    return top_posts
