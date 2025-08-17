from flask import Blueprint, render_template, jsonify
import Users.py

# The file is all about routing traffic to the correct urls
# Ai was used for some of the more complicated routing like roomNum


main = Blueprint('main', __name__)


@main.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@main.route("/canvas", methods=["GET"])
def canvas():
    return render_template("canvas.html")


@main.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    # call create user login.
    return "Success"

@main.route("/users" methods=["GET", "POST"])
async def login():
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    if not user or user["password"] != password:
        raise HTTPExpection(status_code=401, "Incorrect user or password")
    token = generate_token(username)
    return 



@main.route("/room/<username>", methods=["POST"])
def create_room(username):

    return 0


@main.route("/room/<int:roomNum>", methods=["GET"])
def room(roomNum):
    #Change this obviously
    return render_template("canvas.html", room_id=roomNum)

@main.route("/room/<int:roomNum>/users", methods=["GET"])
def get_users(roomNum):
    users = get_users(roomNum)
    # Will require further exploration. But the idea is to be able to see who is in the room so they can receive room data for example drawing. Will need to track leaving probably with websockets tho.
    return jsonify({"room": roomNum, "users": users})


@main.route("/user/<username>", methods=["DELETE"])
def delete_user(username):
    return 0

@main.route("/room/<pageJSN>", methods=["GET"])
def get_page_json(pageJSN):
    return "Success" 
