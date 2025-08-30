import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

users_map = {
    "user": {"password": "user123", "role": "USER"},
    "admin": {"password": "admin123", "role": "ADMIN"}
}

def generate_token(username):
    user = users_map.get(username)
    if not user:
        return None

    payload = {
        "username": username,
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=20)
    }

    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

# Chatgpt reference
# Decodes token so we can verify role 
def verify_token(token):
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def guest_login():
    payload = {
        "username": "Guest" + str(int(datetime.now().timestamp()) >> 4),
        "role": "GUEST",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=20)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token



