from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')


def sentiment_analysis(topics):
    print(f"Amount of topics: {len(topics)}")
    
    
    sid_obj = SentimentIntensityAnalyzer()
    
    for topic in topics[:10]:
        print(f"Topic: {topic['topic']}")
        print(f"Amount of posts: {len(topic['posts'])}")
        
        total_compound = 0
        total_neg = 0
        total_neu = 0
        total_pos = 0
        count = 0

        for post in topic['posts']:
            for comment in post['comments']:
                sentiment = sid_obj.polarity_scores(comment)
                # print(f"Post: {post}")
                
                # print(f"Sentiment Scores: {sentiment}")
                # print(f"Negative Sentiment: {sentiment['neg']*100:.2f}%")
                # print(f"Neutral Sentiment: {sentiment['neu']*100:.2f}%")
                # print(f"Positive Sentiment: {sentiment['pos']*100:.2f}%")
                
                # if sentiment['compound'] >= 0.05:
                #     print("Overall Sentiment: Positive")
                # elif sentiment['compound'] <= -0.05:
                #     print("Overall Sentiment: Negative")
                # else:
                #     print("Overall Sentiment: Neutral")

                total_compound += sentiment['compound']
                total_neg += sentiment['neg']
                total_neu += sentiment['neu']
                total_pos += sentiment['pos']
                count += 1
    
        if count > 0:
            print(f"\n--- Averages for topic '{topic['topic']}' ---")
            print(f"Average compound: {total_compound / count:.3f}")
            print(f"Average negative: {total_neg / count * 100:.2f}%")
            print(f"Average neutral:  {total_neu / count * 100:.2f}%")
            print(f"Average positive: {total_pos / count * 100:.2f}%")
            print(f"The average is based on {count} comments.")

            if total_compound / count >= 0.05:
                print("Overall Sentiment: Positive\n")
            elif total_compound / count <= -0.05:
                print("Overall Sentiment: Negative\n")
            else:
                print("Overall Sentiment: Neutral\n")
        else:
            print("No posts to analyze for this topic.\n")
        
                        