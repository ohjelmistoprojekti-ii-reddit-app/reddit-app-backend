import asyncio
import random
from app.services.reddit_api import get_posts
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis

# used for viewing reddit posts and topic modeling results in terminal

async def demo():
    # get_posts(<subreddit>, <type of posts>, <number of posts>)
    # type of post can be: controversial, gilded, hot, new, rising or top
    posts = await get_posts("all", "hot", 1000)

    random_posts = random.sample(posts, 3)
    print("EXAMPLE POSTS:")
    for i, post in enumerate(random_posts):
            print(f"{i+1}. {post['title']}")
            if post['content']: print(f"CONTENT: {post['content']}")
            if post['comments']: print(f"EXAMPLE COMMENT: {post['comments'][0]}")
            print(f"UPVOTES: {post['score']} | COMMENTS: {post['num_comments']}\n")
    print("-" * 30)

    topics = extract_topics(posts)

    print("EXAMPLE TOPICS:")
    for topic in topics[:10]:
        print(f"{topic['id']+1}. {topic['topic']}\n")
        print(f"POSTS UNDER THIS TOPIC: {topic['num_posts']}\n")
        print("EXAMPLE POSTS:\n")
        for post in topic['posts'][:2]:
            print(f"TITLE: {post['title']}")
            if post['content']: print(f"CONTENT: {post['content']}")
            print(f"EXAMPLE COMMENT: {post['comments'][0]}")
            print(f"UPVOTES: {post['score']}")
            print("---")
        print()

    analyzed_topics = sentiment_analysis(topics)

if __name__ == "__main__":
    asyncio.run(demo())