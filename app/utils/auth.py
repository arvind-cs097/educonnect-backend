from flask import current_app
import jwt
from datetime import datetime, timedelta, timezone

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    SECRET_KEY = current_app.config["SECRET_KEY"]
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
