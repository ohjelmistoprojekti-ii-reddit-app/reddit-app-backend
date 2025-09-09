from app.helpers.text_processing import preprocess
from app.helpers.stopwords import stopwords
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from hdbscan import HDBSCAN
from umap import UMAP
import datetime

# TODO: summarize the topics with AI

def extract_topics(posts):
    print("Extracting topics..")
    start = datetime.datetime.now()

    # clean up data
    docs = preprocess(posts)

    # for clustering
    hdbscan_model = HDBSCAN(
        min_cluster_size=5, # min amount of posts in a cluster (topic); if cluster has less posts, it is discarded
        min_samples=2, # smaller value allows more clusters and less noise
        prediction_data=True,
        metric='euclidean'
    )

    # for dimensionality reduction: makes clustering easier and faster
    umap_model = UMAP(
        n_neighbors=10, # controls topic scope: higher (10+) = broader themes, lower (~5) = small, niche discussions
        metric='cosine'
    )

    model = BERTopic(
        embedding_model="all-MiniLM-L12-v2", # hugging face sentence transformers model for embedding
        hdbscan_model=hdbscan_model,
        umap_model=umap_model
    )

    topics, probs = model.fit_transform(docs)

    # remove irrelevant words from the topics
    vectorizer_model = CountVectorizer(stop_words=stopwords())
    model.update_topics(docs, vectorizer_model=vectorizer_model)

    print(model.get_topic_info())

    end = datetime.datetime.now()
    print(f"Topic modeling duration: {end - start}\n")

    topic_with_posts = {}
    results = []

    for topic_id in topics:
        if topic_id == -1:
            continue # skip noise

        # initialize a list to store posts for each topic
        topic_with_posts[topic_id] = []

    for i, topic_id in enumerate(topics):
        if topic_id == -1:
            continue
        
        # link post to the right topic
        topic_with_posts[topic_id].append(posts[i])
    
    for topic_id, topic_posts in topic_with_posts.items():
        topic_list = model.get_topic(topic_id)
        topic_words = [word for word, prob in topic_list[:3]]
        
        results.append({
            "id": topic_id,
            "topic": topic_words,
            "num_posts": len(topic_posts), # amount of posts in this category
            "posts": topic_posts
        })

    return sorted(results, key=lambda k: k['id'])

