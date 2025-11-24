from app.config import Config

def get_country_subreddit(login_required):
    subreddit = None
    for item in Config.COUNTRY_SUBREDDITS:
        if item['login_required'] == login_required:
            subreddit = item['subreddit']
            break
    return subreddit

def register_user(client, username, email, password):
    return client.post(
        "/api/authentication/register",
        json={"username": username,"email": email,"password": password}
    )

def login_user(client, username, password):
    return client.post(
        "/api/authentication/login",
        json={"username": username,"password": password}
    )