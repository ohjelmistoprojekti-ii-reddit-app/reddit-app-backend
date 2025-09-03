import asyncio
from app.services.reddit_api import get_posts

async def main():
    # get_posts(<subreddit>, <number of posts>)
    # try it out by changing the parameters
    posts = await get_posts("movies", 10)

    for i, post in enumerate(posts):
        print(f"{i+1}. {post['title']}")
        if post['content']: print(f"> {post['content']}\n")
        print(f"- Post score: {post['score']} | Comments: {post['num_comments']}\n")

if __name__ == "__main__":
    asyncio.run(main())