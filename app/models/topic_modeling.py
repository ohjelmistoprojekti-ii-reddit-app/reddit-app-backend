from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from hdbscan import HDBSCAN
import datetime
import re

# WORK IN PROGRESS

# TODO: filter out or translate languages other than english
# TODO: get a better stopword list
# TODO: summarize the topics with AI?

def preprocess(posts):
    processed = []

    for post in posts:
        post_parts = [post['title'], post['content']]

        for comment in post['comments']:
            if comment and len(comment) > 10: # remove empty and short comments
                post_parts.append(comment)

        combined = " ".join(post_parts) # join a post into one string, separated by spaces
        combined = re.sub(r'https?://\S+|www\.\S+', '', combined) # remove links
        processed.append(combined)
    
    return processed

def extract_topics(posts):
    print("Extracting topics..")
    start = datetime.datetime.now()

    # clean up data
    docs = preprocess(posts)

    # for clustering
    hdbscan_model = HDBSCAN(
        min_cluster_size=5, # min amount of posts in a topic
        prediction_data=True
    )

    model = BERTopic(
        embedding_model="all-MiniLM-L12-v2", # hugging face sentence transformers for embedding
        hdbscan_model=hdbscan_model
    )

    topics, probs = model.fit_transform(docs)

    # remove irrelevant words from the topics
    vectorizer_model = CountVectorizer(stop_words="english")
    model.update_topics(docs, vectorizer_model=vectorizer_model)

    print(model.get_topic_info())

    end = datetime.datetime.now()
    print(f"Topic modeling duration: {end - start}\n")

    topic_with_posts = {}
    results = []

    for topic_id in topics:
        if topic_id == -1:
            continue  # skip noise

        # initialize a list for original post information
        topic_with_posts[topic_id] = []

    for i, topic_id in enumerate(topics):
        if topic_id == -1:
            continue  # skip noise

        # link post to the right topic
        topic_with_posts[topic_id].append(posts[i])
    
    for topic_id, topic_posts in topic_with_posts.items():
        topic_list = model.get_topic(topic_id)
        topic_words = [word for word, prob in topic_list[:3]]
        
        results.append({
            "id": topic_id,
            "topic": topic_words,
            "posts": topic_posts
        })

    return sorted(results, key=lambda k: k['id'])











