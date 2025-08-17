import jwt
from datetime import datetime, timedelta, timezone
import os
from __init__ import app


users_map = {"user": {"password": "user123", "role": "USER"},
             "admin": {"password": "admin123", "role": "ADMIN"}
            }

#Reference to week 4 practical from Alan
def generate_token(username):
    user = users_map.get(username)
    if not user:
        return None

    payload = {
        'username': username,
        'role': user["role"],
        'exp': datetime.now(timezone.utc) + timedelta(minutes=20)
    }
    token = jwt.encode(payload, app.secret_key, algorithm="HS256")
    return token


def verify_token(token: str):
    try:
        decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def guest_login():
    payload = {
        'username': "Guest" + str(int(datetime.now().timestamp()) >> 4),
        'role': "guest",
        'exp': datetime.now(timezone.utc) + timedelta(minutes=20)
    }
    token = jwt.encode(payload, app.secret_key, algorithm="HS256")
    return token
