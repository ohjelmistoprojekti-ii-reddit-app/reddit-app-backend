import asyncio
import os
import asyncpraw
import datetime
from dotenv import load_dotenv
from app.helpers.text_processing import is_bot


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


async def process_submission(submission, semaphore):
    async with semaphore:
        try:
            await submission.load()
            await submission.comments.replace_more(limit=0)

            comments = []
            count = 0
            for comment in submission.comments:
                if not is_bot(comment.body.lower()): # leave out bot comments
                    comments.append(comment.body)
                    count += 1
                    if count >= 8:
                        break

            return {
                "id": submission.id,
                "subreddit": submission.subreddit.display_name,
                "title": submission.title,
                "content": submission.selftext,
                "comments": comments,
                "num_comments": submission.num_comments,
                "score": submission.score,
                "upvote_ratio": submission.upvote_ratio,
                "created_at": datetime.datetime.fromtimestamp(submission.created_utc, tz=datetime.timezone.utc),
                "link": f"https://reddit.com{submission.permalink}",
                "content_link": submission.url
            }
        except Exception as e:
            print(f"Error processing submission {submission.id}: {e}")
            return None

# max_concurrent_requests smaller value = slower fetching, but less chance of going over rate limit

async def get_posts(subreddit_name, post_type, limit_num, max_concurrent_requests):
    start = datetime.datetime.now()
    print(f"Fetching posts..")

    reddit = await create_client()
    subreddit = await reddit.subreddit(subreddit_name)
    semaphore = asyncio.Semaphore(max_concurrent_requests) 

    submissions = []
    async for submission in getattr(subreddit, post_type)(limit=limit_num):
        submissions.append(submission)

    tasks = []
    for submission in submissions:
        task = process_submission(submission, semaphore)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)

    posts = []
    for post in results:
        if post is not None:
            posts.append(post)

    await reddit.close()

    end = datetime.datetime.now()
    print(f"Fetched {len(posts)} posts in {end - start}.")

    return posts