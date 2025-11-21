from app.config import Config

def get_country_subreddit(login_required):
    for item in Config.COUNTRY_SUBREDDITS:
        if item['login_required'] == login_required:
            subreddit = item['subreddit']
            break
    return subreddit