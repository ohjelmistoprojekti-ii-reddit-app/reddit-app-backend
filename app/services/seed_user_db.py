from app.services.db import get_db
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

def seed_users():
    db, client = get_db()
    try:
        if db.users.count_documents({}) == 0:
            last_user = db.users.find_one(sort=[("user_id", -1)])
            if not last_user:
                next_user_id = 1 
            else:
                next_user_id = last_user["user_id"] + 1

            user1_password = generate_password_hash(os.getenv("SEED_USER_1_PASSWORD"))
            user2_password = generate_password_hash(os.getenv("SEED_USER_2_PASSWORD"))

            db.users.insert_many([
                {"id": next_user_id, "username": "johnd", "email": "johnd@example.com", "password": user1_password},
                {"id": next_user_id + 1, "username": "saral", "email": "saral@example.com", "password": user2_password},
            ])
            print("Sample users inserted into MongoDB")
        else:
            print("Users already exist, skipping seeding")
    finally:
        client.close()

if __name__ == "__main__":
    seed_users()