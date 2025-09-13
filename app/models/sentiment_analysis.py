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

        analyzed_topics.append({
            "id": topic['id'],
            "topic": topic['topic'],
            "num_posts": topic['num_posts'],
            "posts": topic['posts'][:2],
            "sentiment_values": {
                "average_compound": round(average_compound, 3),
                "average_neg": round(average_neg, 3),
                "average_neu": round(average_neu, 3),
                "average_pos": round(average_pos, 3),
                "comment_count": count
            }
        })

    return analyzed_topics
        
        
                        