from flask import Blueprint, jsonify
import asyncio
from app.services.reddit_api import get_posts
from app.helpers.post_util import get_top_posts_with_translations
from app.helpers.translation import translate_label_or_topic
from app.models.topic_modeling import extract_topics
from app.models.sentiment_analysis import sentiment_analysis

bp = Blueprint('test', __name__, url_prefix='/test')

# Test route for country subreddit analysis: topic modeling, translation, sentiment analysis
@bp.route('/<id>/<name>/<subreddit>', methods=['GET'])
def test(id, name, subreddit):
    posts = asyncio.run(get_posts(subreddit, "hot", 400, 2))
    topics = extract_topics(posts)
    topics = topics[:4] # Limit to top 4 topics
    
    try:
        print("Translating posts..")
        for topic in topics:
            topic['posts'] = topic['posts'][:1] # Translate 1 post per topic

            # Translate topic label and topic words
            translated_label = translate_label_or_topic(label=topic['label'])
            topic['label_eng'] = translated_label

            translated_topic = translate_label_or_topic(topic=topic['topic'])
            topic['topic_eng'] = translated_topic

            posts_with_translations = asyncio.run(get_top_posts_with_translations(topic['posts']))
            if len(posts_with_translations) > 0:
                topic['posts'] = posts_with_translations

    except Exception as e:
        print("Error while translating:", e)

    analyzed_topics = sentiment_analysis(topics)
    for topic in analyzed_topics:
        topic['country_id'] = id
        topic['country_name'] = name

    return jsonify(analyzed_topics), 200