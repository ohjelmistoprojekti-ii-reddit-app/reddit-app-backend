import asyncio
from datetime import datetime, timezone
from app.helpers.post_util import get_top_posts_with_translations
from app.services.reddit_api import get_posts
from app.models.sentiment_analysis import sentiment_analysis_for_map_feature
from app.services.db import save_data_to_database
from app.config import Config
import sys


"""
For GitHub Actions workflow:
Fetches, translates and analyzes posts from the given country subreddits, and inserts the results into the database

Usage: python -m scripts.countries_pipeline
"""

async def countries_pipeline(country_id, country_name, subreddit):
    print(f"===== PROCESSING SUBREDDIT: {subreddit} =====")
    
    try:
        posts = await get_posts(subreddit, "hot", 10, 2)
        top_posts = await get_top_posts_with_translations(posts, n_posts=3)

        analyzed_posts = sentiment_analysis_for_map_feature(top_posts)
        
        combined_data = {
            "country_id": country_id,
            "country_name": country_name,
            "posts": analyzed_posts,
            "subreddit": subreddit,
            "timestamp": datetime.now(timezone.utc)
        }

        save_data_to_database([combined_data], "countries")
        return True
    except Exception as e:
        print(f"::error::Pipeline failed for '{subreddit}': {e}")
        return False

if __name__ == "__main__":
    country_data = Config.COUNTRY_SUBREDDITS

    failure = False

    for country in country_data:
        success = asyncio.run(countries_pipeline(country['id'], country['name'], country['subreddit']))
        if success:
            print(f"✔️  Successfully analyzed '{country['subreddit']}'\n")
        else:
            failure = True

    # Make sure that GitHub Actions workflow fails if any subreddit processing fails
    if failure:
        sys.exit(1)
