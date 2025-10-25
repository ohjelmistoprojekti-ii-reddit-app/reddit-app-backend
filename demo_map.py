import asyncio
from app.services.reddit_api import get_posts
from app.helpers.suomi_dataset import suomi_dataset
from app.helpers.post_util import get_top_posts_with_translations
from app.helpers.translation import translate_label_or_topic
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis, sentiment_analysis_for_map_feature

"""
You can use this file to test topic modeling, translation, and sentiment analysis for the map feature.

For some reason some of the translation results do not always show up correctly, for example label_eng or topic_eng may be missing.

NOTE: The quality of the results for this pipeline is currently lower than expected, and this solution should not be used in production as is.
After including topic modeling, we need to translate even more content, which brings to light the limitations of the current translation system.
So, the main problem is that the translations are not accurate enough when analyzing topics from multiple languages.

If we can improve the translation quality, this pipeline could be useful in the future.

NOTE: You can also test this version via the /test/<id>/<name>/<subreddit> route in test_routes.py
"""

async def demo_map(country_id, country_name, subreddit):

    # posts = await get_posts(subreddit, "hot", 500, 2)
    posts = suomi_dataset
    topics = extract_topics(posts)
    topics = topics[:3] # Limit to top 3 topics for the demo
    
    try:
        print("Translating posts..")
        for topic in topics:
            topic['posts'] = topic['posts'][:1]

            translated_label = translate_label_or_topic(label=topic['label'])
            topic['label_eng'] = translated_label

            translated_topic = translate_label_or_topic(topic=topic['topic'])
            topic['topic_eng'] = translated_topic

            posts_with_translations = await get_top_posts_with_translations(topic['posts'])
            if len(posts_with_translations) > 0:
                topic['posts'] = posts_with_translations

    except Exception as e:
        print("Error while translating:", e)

    print(topics[0])

    analyzed_topics = sentiment_analysis(topics)
    for topic in analyzed_topics:
        topic['country_id'] = country_id
        topic['country_name'] = country_name
    
    return analyzed_topics
    

if __name__ == "__main__":
    country_data = [
        { "id": "FI", "name": "Finland", "subreddit": "suomi" },
    ]

    data = []
    for country in country_data:
        print(f"===== COUNTRY SUBREDDIT DEMO: {country['subreddit']} =====")
        data = asyncio.run(demo_map(country['id'], country['name'], country['subreddit']))

    for topic in data:
        print(f"----- {topic['topic_id']+1}. {topic['label']}")
        print(f"In English: {topic.get('label_eng', 'No translation available')}")
        print(f"Topic words: {topic['topic']}")
        print(f"In English: {topic.get('topic_eng', 'No translation available')}")
        print(f"Example posts:")
        for post in topic['posts']:
            print(f"Title: {post['title']}")
            print(f"--> Eng title: {post.get('title_eng', 'No translation available')}")
            if post['content']:
                print(f"Content: {post['content']}")
            print(f"--> Eng content: {post.get('content_eng', 'No translation available')}")
            print(f"Score: {post['score']}\n")


# subreddits = [
#     "suomi",
#     "sweden",
#     "italia",
#     "mexico",
#     "spain",
#     ]

# async def demo_map():

#     for subreddit in subreddits:
        
#         posts = await get_posts(subreddit, "hot", 10, 4)
#         top_posts = await get_top_posts_with_translations(posts)
        
#         analyzed_top_posts = sentiment_analysis_for_map_feature(top_posts)
#         print(analyzed_top_posts)
    

# if __name__ == "__main__":
#     asyncio.run(demo_map())