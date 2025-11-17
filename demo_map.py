# import asyncio
# from app.services.reddit_api import get_posts
# from app.models.sentiment_analysis import sentiment_analysis_for_map_feature
# from app.helpers.post_util import get_top_posts_with_translations

# # Try out the current country subreddit analysis pipeline by running:
# # python demo_map.py

# async def demo_map(country_id, country_name, subreddit):

#     print(f"===== Analyzing subreddit: {subreddit} =====")

#     posts = await get_posts(subreddit, "hot", 10, 2)
#     top_posts = await get_top_posts_with_translations(posts, n_posts=3)

#     analyzed_posts = sentiment_analysis_for_map_feature(top_posts)
    
#     combined_data = {
#         "country_id": country_id,
#         "country_name": country_name,
#         "posts": analyzed_posts,
#         "subreddit": subreddit,
#     }
    
#     return combined_data

# if __name__ == "__main__":
#     country_data = [
#         { "id": "FI", "name": "Finland", "subreddit": "suomi" },
#         { "id": "AU", "name": "Australia", "subreddit": "australia"},
#     ]

#     for country in country_data:
#         data = asyncio.run(demo_map(country['id'], country['name'], country['subreddit']))

#         print(f"\nEXAMPLE POSTS:")
#         for post in data['posts']:
#             print(f"TITLE: {post['title']}")
#             if post['title_eng']:
#                 print(f"TITLE IN ENGLISH: {post['title_eng']}\n")

#             print(f"EXAMPLE COMMENTS:")
#             for comment in post['comments']:
#                 print(f"- {comment}")
            
#             if post['comments_eng']:
#                 print(f"COMMENTS IN ENGLISH:")
#                 for comment in post['comments_eng']:
#                     print(f"- {comment}")
#             print("\n--------\n")
