import asyncio
from app.services.reddit_api import get_posts
from app.helpers.post_util import get_top_posts_with_translations
from app.helpers.translation import translate_label_or_topic
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis
from app.services.db import save_posts_to_database
from app.config import Config
import sys

"""
For GitHub Actions workflow:
Fetches, translates and analyzes posts from the country subreddits, and inserts the results into the database

NOTE: No workflow is currently set up to run this pipeline automatically.
When implementing the workflow, make sure to run the subreddit sets at different times, as this pipeline fetches a lot of data and may hit Reddit API rate limits.

To test this pipeline manually, run:
    python -m scripts.country_topics_pipeline

NOTE: The quality of the results for this pipeline is currently lower than expected, and this should not be used in production as is.
The main problem is the translations. If we can improve the translation quality, this pipeline could be useful in the future.
"""

async def country_topics_pipeline(country_id, country_name, subreddit):
    print(f"===== PROCESSING SUBREDDIT: {subreddit} =====")
    
    try:
        posts = await get_posts(subreddit, "hot", 400, 2)
        
        topics = extract_topics(posts)
        topics = topics[:5] # Limit to top 5 topics
        
        try:
            print("Translating posts..")
            for topic in topics:
                topic['posts'] = topic['posts'][:1] # Limit to top 1 post per topic

                translated_label = translate_label_or_topic(label=topic['label'])
                topic['label_eng'] = translated_label

                translated_topic = translate_label_or_topic(topic=topic['topic'])
                topic['topic_eng'] = translated_topic

                posts_with_translations = await get_top_posts_with_translations(topic['posts'])
                if len(posts_with_translations) > 0:
                    topic['posts'] = posts_with_translations
        except Exception as e:
            print("Error while translating:", e)

        analyzed_topics = sentiment_analysis(topics)
        for topic in analyzed_topics:
            topic['country_id'] = country_id
            topic['country_name'] = country_name

        # NOTE: currently using test db collection
        save_posts_to_database(analyzed_topics, subreddit, "countries_test")
        return True
    except Exception as e:
        print(f"::error::Pipeline failed for '{subreddit}': {e}")
        return False

if __name__ == "__main__":
    """
    Usage: python -m scripts.countries_pipeline [--set1 | --set2]
    Pass '--set1' or '--set2' as a command-line argument to select which country subreddit set to process.
    """

    if "--set1" in sys.argv[1:]:
        country_data = Config.COUNTRY_SUBREDDITS_SET1
    elif "--set2" in sys.argv[1:]:
        country_data = Config.COUNTRY_SUBREDDITS_SET2
    else:
        print("::warning::No valid cmd argument provided. Use '--set1' or '--set2' to select a country set.")
        print("Running pipeline with test data.")
        country_data = [
            { "id": "FI", "name": "Finland", "subreddit": "suomi" },
            { "id": "AU", "name": "Australia", "subreddit": "australia" },
        ]

    failure = False

    for country in country_data:
        success = asyncio.run(country_topics_pipeline(country['id'], country['name'], country['subreddit']))
        if success:
            print(f"✔️  Successfully analyzed '{country['subreddit']}'\n")
        else:
            failure = True

    # Make sure that GitHub Actions workflow fails if any subreddit processing fails
    if failure:
        sys.exit(1)