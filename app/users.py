from enum import Enum

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
