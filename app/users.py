from enum import Enum
import jwt
import datetime
import os
from __init__.py import app

directoryPath = os.path(os.path.dirname(__file__), "templates")
app.mount("/templates", Staticfiles(directory=directoryPath), name="templates")
security = HTTPBearer()


guestNum = 0

class Permission(Enum):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"


class Account:
    def __init__(self, username: str, password: str, email: str, permission: Permission):
        self.username = username
        self.password = password
        self.email = email
        self.permission = permission


    def setPermission(self, permission):
        self.permission = permission

    def getPermission(self):
        return self.permission 


    def selected_guest():
        global guestNum
        guest = Account("guest" + str(guestNum), "", "", Permission.GUEST)
        guestNum += 1

        
    def create_account(username, password, email):
        account = Account(username, password, email, Permission.USER)
    

user = Account("user", "user123", "user@user.com", Permission.USER)
admin = Account("admin", "admin123", "admin@admin.com", Permission.ADMIN)


users_map = {"user": user,
              "admin": admin}

#Reference to week 4 practical from Alan
def generate_token():
    payload = {
        'username': username,
        'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=20)
    }
    token = jwt.encode(payload, app.secret_key, algorithm="HS256")
    return token

#Reference to week 4 practical from Alan
def auth_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or not credentials.scheme == "Bearer":
        raise HTTPException(status_code=401, details="unauthorized")

    token = credentials.credentials
    try:
        user = jwt.decode(token, app.secret_key, algorithm=["HS256"])
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid token")


