import asyncio
import random
from app.services.reddit_api import get_posts
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis
import datetime

# used for viewing reddit posts and topic modeling results in terminal

async def demo():
    # get_posts(<subreddit>, <type of posts>, <number of posts>)
    # type of post can be: controversial, gilded, hot, new, rising or top
    posts = await get_posts("all", "hot", 500, 2)

    random_posts = random.sample(posts, 3)
    print("EXAMPLE POSTS:")
    for i, post in enumerate(random_posts):
            print(f"{i+1}. {post['title']}")
            if post['content']: print(f"CONTENT: {post['content']}")
            if post['comments']: print(f"EXAMPLE COMMENT: {post['comments'][0]}")
            print(f"UPVOTES: {post['score']} | COMMENTS: {post['num_comments']}\n")
    print("-" * 30)

    topics = extract_topics(posts)
    analyzed_topics = sentiment_analysis(topics)

    print(analyzed_topics)
    
    
    print(f"Amount of topics: {len(topics)}")
    print("> EXAMPLE TOPICS::")
    for topic in analyzed_topics[:4]:
        print(f"{topic['topic_id']}. {topic['topic']}\n")
        print(f"POSTS UNDER THIS TOPIC: {topic['num_posts']}\n")
        print("EXAMPLE POSTS:\n")
        for post in topic['posts'][:2]:
            print(f"TITLE: {post['title']}")
            if post['content']: print(f"CONTENT: {post['content']}")
            print(f"EXAMPLE COMMENT: {post['comments'][0]}")
            print(f"UPVOTES: {post['score']}")
            print("---")
        
        s = topic['sentiment_values']
        if s['comment_count'] > 0:
            print(f"Average compound: {s['average_compound']}")
            print(f"Average negative: {s['average_neg']}%")
            print(f"Average neutral:  {s['average_neu']}%")
            print(f"Average positive: {s['average_pos']}%")
            print(f"The average is based on {s['comment_count']} comments.")

            if s['average_compound'] >= 0.05:
                print("Overall Sentiment: Positive\n")
            elif s['average_compound'] <= -0.05:
                print("Overall Sentiment: Negative\n")
            else:
                print("Overall Sentiment: Neutral\n")
        
        else:
            print("No posts to analyze for this topic.\n")
          

if __name__ == "__main__":
    asyncio.run(demo())