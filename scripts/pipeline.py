import asyncio
import datetime
from app.services.reddit_api import get_posts
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis
from app.services.db import save_posts_to_database

subreddits = [
    "worldnews",
    "technology",
    "entertainment",
    "movies",
    "gaming",
    "sports",
    "travel",
    "jobs",
    "futurology",
    "programming",
]

# for github actions workflow
# fetches and analyzes posts from the given subreddits
# and inserts the results into the database
def pipeline(subreddits):
    for subreddit in subreddits:
        print(f"===== PROCESSING SUBREDDIT: {subreddit} =====")
        
        try:
            posts = asyncio.run(get_posts(subreddit, "hot", 500, 2))
        except Exception as e:
            print(f"::error::Error fetching posts: {e}")
            return

        try:
            topics = extract_topics(posts)
        except Exception as e:
            print(f"::error::Error extracting topics: {e}")
            return

        try:
            analyzed_topics = sentiment_analysis(topics)
        except Exception as e:
            print(f"::error::Error analyzing sentiment: {e}")
            return

        try:
            # add subreddit and run timestamp to each topic for easier db filtering
            for topic in analyzed_topics:
                topic["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
                topic["subreddit"] = subreddit

            save_posts_to_database(analyzed_topics, "posts")
        except Exception as e:
            print(f"::error::Error inserting into database: {e}")
        
    print("Analysis complete.")

if __name__ == "__main__":
    pipeline(subreddits)