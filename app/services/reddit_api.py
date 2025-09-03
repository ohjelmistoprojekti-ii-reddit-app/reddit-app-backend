import os
from dotenv import load_dotenv
import asyncpraw
import asyncio

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

async def get_posts(subreddit_name, limit_num):
    reddit = await create_client()

    posts = []
    subreddit = await reddit.subreddit(subreddit_name)

    # currently fetching "hot" posts
    # you can also try these: controversial, gilded, hot, new, rising, top
    async for submission in subreddit.hot(limit=limit_num):
        posts.append({
            "title": submission.title,
            "content": submission.selftext,
            "num_comments": submission.num_comments,
            "score": submission.score
        })

    await reddit.close()
    return posts