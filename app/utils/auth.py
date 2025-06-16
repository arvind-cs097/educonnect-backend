import os
import jwt
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    print("Secret Key", SECRET_KEY)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
