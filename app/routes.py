from flask import Blueprint, render_template, jsonify, request, send_file
from io import BytesIO
from .users import generate_token, users_map, verify_token
from .export import * 
import base64
import random

# The file is all about routing traffic to the correct urls
# Ai was used for some of the boilery-plate stuff. 


main = Blueprint('main', __name__)


@main.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@main.route("/userLogged", methods=["GET"])
def userLogged():
    # Cookie related boilerplate influenced by chatgpt
    token = request.args.get("token")
    jsonToken = verify_token(token)

    if jsonToken.get("role") != "USER" and jsonToken.get("role") != "ADMIN":
        return render_template("/")

    if jsonToken.get("role") == "ADMIN":
        return render_template("adminLogged.html")
    #Need to verify that token is logged in as a user 

    return render_template("userLogged.html")

@main.route("/adminLogged", methods=["GET"])
def adminLogged():
    # Get logged token
    token = request.args.get("token")
    jsonToken = verify_token(token)

    if jsonToken.get("role") == "ADMIN":
        return render_template("adminLogged.html")

    else:
        return render_template("/")


@main.route("/canvas", methods=["GET"])
def canvas():
    roomID = request.args.get("roomID")

    return render_template("canvas.html", roomID=roomID)


@main.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    # call create user login.
    return "Success"

@main.route("/users", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = users_map.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Incorrect username or password"}), 401

    token = generate_token(username)
    return jsonify({"token": token})



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


@main.route("/room/export", methods=["POST"])
def export():
    data = request.get_json()
    strokes = data.get("history", [])
    canvasW = data.get("canvasWidth")
    canvasH = data.get("canvasHeight")

    
    if len(strokes) == 0:
        print("Empty List", flush=True)

    photos = render_strokes(strokes, canvasH, canvasW)


    return send_file(
        photos,
        mimetype='application/pdf',
        as_attachment=True,
        download_name="canvas_export.pdf"
    )


@main.route("/admin/stress", methods=["POST"])
def stress():
    canvasW = 1080
    canvasH = 720
    coords = []
    num = 1
    jsonList = []

    pageAmount = 1000

    for x in range(pageAmount):
        for i in range(canvasW):
            for j in range(canvasH):
                # Not really uniformDistro but itll work for this purpose
                uniformDistro = random.randint(0,1000)

                if uniformDistro <=  1:
                    coords.append([i, j])

        pageJson = {
            "roomID": 0,
            "canvasRoom": x,
            "strokeID": 0,
            "drawID": num,
            "colour": "black",
            "stroke": cords, 
            "size": 6
        }

        jsonList.append(pageJson)
        num = num + 1
    pass





