import asyncio
from app.services.reddit_api import get_posts
from app.models.sentiment_analysis import sentiment_analysis_for_map_feature
from app.helpers.post_util import get_top_posts_with_translations

subreddits = [
    "suomi",
    "sweden",
    "italia",
    "mexico",
    "spain",
    ]

async def demo_map():

    for subreddit in subreddits:
        
        posts = await get_posts(subreddit, "hot", 10, 4)
        top_posts = await get_top_posts_with_translations(posts)
        
        analyzed_top_posts = sentiment_analysis_for_map_feature(top_posts)
        print(analyzed_top_posts)
    

if __name__ == "__main__":
    asyncio.run(demo_map())