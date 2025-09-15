import os
import asyncpraw
import datetime
from dotenv import load_dotenv
from app.helpers.text_processing import is_bot

# after fetching post comments, fetch became super slow. still, we need the comments for the sentiment analysis
# TODO: try to find a way to make the API connection faster

load_dotenv()

async def create_client():
    if not all([os.getenv("REDDIT_CLIENT_ID"), os.getenv("REDDIT_CLIENT_SECRET"), os.getenv("REDDIT_USER_AGENT")]):
        raise ValueError("Reddit API credentials missing in .env")

    reddit = asyncpraw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )
    return reddit

async def get_posts(subreddit_name, post_type, limit_num):
    start = datetime.datetime.now()
    print(f"Fetching.. This will take a while.")
    reddit = await create_client()

    posts = []
    subreddit = await reddit.subreddit(subreddit_name)

    async for submission in getattr(subreddit, post_type)(limit=limit_num):
        await submission.load() # needed for fetching comments

        comments = []
        if submission.num_comments > 0:
            count = 0
            # only top level comments
            for comment in submission.comments:
                if not is_bot(comment.body.lower()): # leave out bot comments
                    comments.append(comment.body)
                    count += 1

                    if count >= 10:
                        break

        posts.append({
            "id": submission.id,
            "title": submission.title,
            "content": submission.selftext,
            "comments": comments,
            "num_comments": submission.num_comments,
            "score": submission.score, # number of upvotes for the post
            "upvote_ratio": submission.upvote_ratio
        })

    end = datetime.datetime.now()
    print(f"Fetch duration: {end - start}")
    print(f"✓ Fetched {len(posts)} posts from r/{subreddit_name}/{post_type}")

    await reddit.close()
    return posts