import jwt
import json
import boto3
from jwt import PyJWKClient
from datetime import datetime, timedelta, timezone
from flask import current_app, request

def load_login_secrets():
    client = boto3.client("secretsmanager", region_name="ap-southeast-2")
    secret_name = "n12197718-whiteboard-assignment"
    response = client.get_secret_value(SecretId = secret_name)
    return json.loads(response["SecretString"])

secrets = load_login_secrets()

#Boilerplate cognito stuff
REGION = "ap-southeast-2"
URL = "https://cognito-idp.ap-southeast-2.amazonaws.com/ap-southeast-2_aqm66hUpn/.well-known/jwks.json"
jwks_client = PyJWKClient(URL)

# Stored secretly
USERPOOL_ID = secrets["USERPOOL_ID"]
CLIENT_ID = secrets["CLIENT_ID"]


# Chatgpt reference
# Decodes token so we can verify role 
def verify_token(token):
    """Verify JWT issued by Cognito"""
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=CLIENT_ID
        )
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Used to get token's cognito group and return the role expected in JWT aka Group: Users = USER
def get_role():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ")[1]
    verifyToken = verify_token(token) # Decodes the token 

    groups = verifyToken.get("cognito:groups", []) # Fetch groups available
    if "Admin" in groups:
        return "ADMIN"
    elif "Users" in groups:
        return "USER"
    else:
        return "GUEST"


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



