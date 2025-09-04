from flask import Blueprint, jsonify
from app.services.reddit_api import get_posts
import asyncio

bp = Blueprint('items', __name__, url_prefix='/items')


# get method for 10 movies
@bp.route('/', methods=['GET'])
def get_items():
    posts = asyncio.run(get_posts("movies", 10))
    return jsonify(posts)

# get method for the subreddit of your choise and the number of posts
@bp.route('/<subreddit>/<int:count>', methods=['GET'])
def get_items_subreddit(subreddit,count):
    posts = asyncio.run(get_posts(subreddit,count))
    return jsonify(posts)


