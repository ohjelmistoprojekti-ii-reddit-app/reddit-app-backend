from app.helpers.text_processing import preprocess, process_topic_label
from app.models.summarizing import summarize_texts
from app.helpers.stopwords import stopwords
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from hdbscan import HDBSCAN
from umap import UMAP
import datetime
from bertopic.representation import KeyBERTInspired
from transformers import pipeline

summarizer = pipeline("summarization", model="google/flan-t5-base")

def extract_topics(posts):
    print("Extracting topics..")
    start = datetime.datetime.now()

    # clean up data
    docs = preprocess(posts)

    # Representation model for better topic labeling
    representation_model = KeyBERTInspired(
        top_n_words=10,
        nr_repr_docs=3,
        nr_samples=300,
        nr_candidate_words=60
    )

    # for clustering
    hdbscan_model = HDBSCAN(
        min_cluster_size=7, # min amount of posts in a cluster (topic); if cluster has less posts, it is discarded
        min_samples=3, # smaller value allows more clusters and less noise
        prediction_data=True,
        metric='euclidean'
    )

    # for dimensionality reduction: makes clustering easier and faster
    umap_model = UMAP(
        n_neighbors=10, # controls topic scope: higher (10+) = broader themes, lower (~5) = small, niche discussions
        n_components=3,
        min_dist=0.0,
        metric='cosine'
    )

    model = BERTopic(
        embedding_model="all-MiniLM-L12-v2", # hugging face sentence transformers model for embedding
        hdbscan_model=hdbscan_model,
        umap_model=umap_model,
        representation_model=representation_model
    )

    topics, probs = model.fit_transform(docs)

    # remove irrelevant words from the topics
    vectorizer_model = CountVectorizer(
        stop_words=stopwords(),
        ngram_range=(1, 2), # Extract both unigrams (single words) and bigrams (pairs of consecutive words) as features
        min_df=2,
        max_df=0.9
    )

    model.update_topics(docs, vectorizer_model=vectorizer_model)
    # Combine similar topics
    print(model.get_topic_info())
    model = model.reduce_topics(docs, nr_topics="auto")
    topics = model.topics_ 
    # Get presentative comments
    rep_docs_by_topic = model.get_representative_docs()

    print(model.get_topic_info())

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
        if not isinstance(topic_list, list):
            continue

        topic_words = [word for word, prob in topic_list[:6]]
        topic_label = process_topic_label(topic_words)
        
        if topic_id in rep_docs_by_topic and rep_docs_by_topic[topic_id]:
            representative_docs = [doc for doc in rep_docs_by_topic[topic_id]]
            # for i, doc in enumerate (representative_docs):
            #     print(str(i) + '.' + doc)
        
        else:
            representative_docs = []
            print(f"No representative docs for topic {topic_id}")

        if representative_docs:
            summarized_text = summarize_texts(representative_docs, summarizer)
        
        else:
            summarized_text = "No representative documents available for this topic."
        
    
        results.append({
            "topic_id": topic_id,
            "topic": topic_words,
            "label": topic_label,
            "summary": summarized_text,
            "num_posts": len(topic_posts), # amount of posts in this category
            "posts": topic_posts
        })

    end = datetime.datetime.now()
    print(f"Topic modeling and summarizing duration: {end - start}")

    return sorted(results, key=lambda k: k['topic_id'])

