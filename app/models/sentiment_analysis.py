from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')


def sentiment_analysis(topics):
    
    sid_obj = SentimentIntensityAnalyzer()
    analyzed_topics = []
    
    for topic in topics[:10]:
                        
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


def sentiment_analysis_top_comments_by_country(comments):
    
    sid_obj = SentimentIntensityAnalyzer()
    analyzed_comments = []
    
    for comment in comments:
        sentiment = sid_obj.polarity_scores(comment['comment_english'])

        analyzed_comments.append({
            "post_title": comment["post_title"],
            "comment_original": comment["comment_original"],
            "comment_eng": comment["comment_english"],
            "post_score": comment["score"],
            "sentiment_values": {
                "sentiment_compound": round(sentiment['compound'], 3),
                "sentiment_neg": round(sentiment['neg'], 3),
                "sentiment_neu": round(sentiment['neu'], 3),
                "sentiment_pos": round(sentiment['pos'], 3),
            },
        })

    return analyzed_comments
        
