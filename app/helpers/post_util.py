from app.helpers.text_processing import is_english, translator


def comments_of_top_posts(posts):
    # Sort posts by Reddit score (upvotes - downvotes), descending
    top_posts = sorted(posts, key=lambda p: p["score"], reverse=True)
    chosen_comments = []

    for post in top_posts[:1]:
        comments = post["comments"]
        if not comments:
            continue
        for comment in comments:
            # excludes links and comments that are difficult to translate due to their length
            if 'http' in comment.lower() or 'www' in comment.lower() or len(comment) > 500:
                continue
            try:
                if is_english(comment):
                    comment_eng = comment
                else:
                    comment_eng = translator(comment)
                chosen_comments.append({
                    "post_title": post["title"],
                    "comment_original": comment,
                    "comment_english": comment_eng,
                    "score": post["score"]
                })
                break  # Only one comment per post
                
            except:
                chosen_comments.append({
                    "post_title": post["title"],
                    "comment_original": comment,
                    "comment_english": "problems with translating",
                    "score": post["score"]
                })
                break

    return chosen_comments