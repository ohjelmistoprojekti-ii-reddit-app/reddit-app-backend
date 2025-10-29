from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

def sentiment_analysis(topics):
    print("Analyzing sentiment..")
    
    sid_obj = SentimentIntensityAnalyzer()
    analyzed_topics = []
    
    for topic in topics:
        total_compound = 0
        total_neg = 0
        total_neu = 0
        total_pos = 0
        count = 0

        for post in topic['posts']:
            for comment in post['comments']:
                sentiment = sid_obj.polarity_scores(comment)

                total_compound += sentiment['compound']
                total_neg += sentiment['neg']
                total_neu += sentiment['neu']
                total_pos += sentiment['pos']
                count += 1

        if count > 0:
            average_compound = total_compound / count
            average_neg = (total_neg / count) * 100
            average_neu = (total_neu / count) * 100
            average_pos = (total_pos / count) * 100
        else:
            average_compound = average_neg = average_neu = average_pos = 0.0

        # Each analyzed topic has two post for performance purposes
        analyzed_topics.append({
            "topic_id": topic['topic_id'],
            "topic": topic['topic'],
            "label": topic['label'],
            "summary": topic['summary'],
            "num_posts": topic['num_posts'],
            "posts": topic['posts'][:2],
            "sentiment_values": {
                "average_compound": round(average_compound, 3),
                "average_neg": round(average_neg, 3),
                "average_neu": round(average_neu, 3),
                "average_pos": round(average_pos, 3),
                "comment_count": count
            },
        })

    return analyzed_topics


def sentiment_analysis_for_map_feature(posts):
    print("Analyzing sentiment..")
    
    sid_obj = SentimentIntensityAnalyzer()
    analyzed_posts = []

    for post in posts:
        
        total_compound = 0
        total_neg = 0
        total_neu = 0
        total_pos = 0
        count = 0

        if post['comments_eng']:
            comments = post['comments_eng']
        else:
            comments = post['comments']

        for comment in comments:
            sentiment = sid_obj.polarity_scores(comment)

            total_compound += sentiment['compound']
            total_neg += sentiment['neg']
            total_neu += sentiment['neu']
            total_pos += sentiment['pos']
            count += 1

        if count > 0:
            average_compound = total_compound / count
            average_neg = (total_neg / count) * 100
            average_neu = (total_neu / count) * 100
            average_pos = (total_pos / count) * 100
        else:
            average_compound = average_neg = average_neu = average_pos = 0.0

        analyzed_posts.append({
            "title": post['title'],
            "title_eng": post['title_eng'],
            "content": post['content'],
            "content_link": post['content_link'],
            "content_eng": post['content_eng'],
            "comments": post['comments'][:3],
            "num_comments": post['num_comments'],
            "comments_eng": post['comments_eng'][:3],
            "score": post["score"],
            "link": post["link"],
            "sentiment_values": {
                "average_compound": round(average_compound, 3),
                "average_neg": round(average_neg, 3),
                "average_neu": round(average_neu, 3),
                "average_pos": round(average_pos, 3)
            },
        })

    return analyzed_posts


def sentiment_analysis_for_posts(posts):
    print("Analyzing sentiment..")
    
    sid_obj = SentimentIntensityAnalyzer()
    analyzed_posts = []

    for post in posts:
        
        total_compound = 0
        total_neg = 0
        total_neu = 0
        total_pos = 0
        count = 0

        for comment in post['comments']:
            sentiment = sid_obj.polarity_scores(comment)

            total_compound += sentiment['compound']
            total_neg += sentiment['neg']
            total_neu += sentiment['neu']
            total_pos += sentiment['pos']
            count += 1

        if count > 0:
            average_compound = total_compound / count
            average_neg = (total_neg / count) * 100
            average_neu = (total_neu / count) * 100
            average_pos = (total_pos / count) * 100
        else:
            average_compound = average_neg = average_neu = average_pos = 0.0

        analyzed_posts.append({
            "title": post['title'],
            "content": post['content'],
            "content_link": post['content_link'],
            "comments": post['comments'][:3],
            "num_comments": post['num_comments'],
            "score": post["score"],
            "link": post["link"],
            "sentiment_values": {
                "average_compound": round(average_compound, 3),
                "average_neg": round(average_neg, 3),
                "average_neu": round(average_neu, 3),
                "average_pos": round(average_pos, 3)
            },
        })

    return analyzed_posts