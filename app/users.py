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
cognito_client = boto3.client("cognito-idp", region_name=REGION) # Probs should be const but to late to change things now. 
# Wrapper for signup - 
cog_wrapper = CognitoIdentityProviderWrapper(cognito_client, USERPOOL_ID, CLIENT_ID)



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
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="RS256")

    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def login_cognito(username, password):
    resp = cognito_client.initiate_auth(
        ClientId = CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
            }
        )
    return resp['AuthenticationResult']['IdToken']


# Lotta reference from https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/cognito/scenario_signup_user_with_mfa.py
def signup_cognito(username, password, email):
    try:
        cog_wrapper.sign_up_user(username, password, email)
        return "Success"
    except Exception as e:
        return {"Error message": str(e)}


def confirm_cognito(username, code):
    try:
        confirmed = cog_wrapper.confirm_user_sign_up(username, code)
        if confirmed:
            allocate_group(username)
            return {"status": "User confirmed"}
        else:
            return {"status": "User failed to confirm"}
    except Exception as e:
        return {"status": str(e)}
    

def allocate_group(username):
    try:
        response = cognito_client.admin_add_user_to_group(
            UserPoolId = USERPOOL_ID,
            Username = username,
            GroupName = "Users"
                )
        return response
    except Exception as e:
        print(f"fatal error allocating to group: {e}")
        return None

def resend_confirmation(username):
    try:
        response = cognito_client.resend_confirmation_code(
            ClientId = CLIENT_ID,
            Username = username
                )
        return {"status": "Code resent"}

    except Exception as e:
        return {"status": str(e)}


        


