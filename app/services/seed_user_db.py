# from app.services.db import connect_db
# from werkzeug.security import generate_password_hash
# from dotenv import load_dotenv
# import os
# import datetime

# load_dotenv()

# def seed_users():
#     client, db = connect_db()
#     try:
#         if db.users.count_documents({}) == 0:
            
#             user1_password = generate_password_hash(os.getenv("SEED_USER_1_PASSWORD"))
#             user2_password = generate_password_hash(os.getenv("SEED_USER_2_PASSWORD"))

#             db.users.insert_many([
#                 {"username": "johnd", "email": "johnd@example.com", "password": user1_password, "last_login": datetime.datetime.now(datetime.timezone.utc), "refresh_revoked": False, "revoked_access_tokens": []},
#                 {"username": "saral", "email": "saral@example.com", "password": user2_password, "last_login": datetime.datetime.now(datetime.timezone.utc), "refresh_revoked": False, "revoked_access_tokens": []},
#             ])
#             print("Sample users inserted into MongoDB")
#         else:
#             print("Users already exist, skipping seeding")
#     finally:
#         client.close()

# if __name__ == "__main__":
#     seed_users()