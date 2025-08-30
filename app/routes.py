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

    return render_template("userLogged.html")

@main.route("/adminLogged", methods=["GET"])
def adminLogged():
    return render_template("adminLogged.html")


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
    canvasW = 1354
    canvasH = 595
    jsonList = []

    pageAmount = 1000

    for page in range(pageAmount):
        # Add each stroke as a separate dictionary
        strokes = [
            {
                "canvas": "-6715537",
                "drawId": 1,
                "strokeId": 0,
                "colour": "black",
                "size": 6,
                "points": [
                    [249, 57],[249, 59],[250, 70],[254, 95],[263, 131],
                    [271, 157],[275, 171],[277, 179],[279, 183]
                ],
                "page": page
            },
            {
                "canvas": "-6715537",
                "drawId": 2,
                "strokeId": 1,
                "colour": "black",
                "size": 6,
                "points": [
                    [361, 57],[361, 58],[361, 61],[361, 68],[361, 82],
                    [364, 105],[369, 132],[374, 154],[377, 166],[378, 174],
                    [380, 178],[380, 180],[380, 181],[380, 181]
                ],
                "page": page
            },
            {
                "canvas": "-6715537",
                "drawId": 3,
                "strokeId": 2,
                "colour": "black",
                "size": 6,
                "points": [
                    [319, 392],[319, 392],[319, 387],[319, 374],[319, 353],
                    [319, 328],[319, 305],[319, 289],[319, 281],[319, 278],
                    [321, 276],[327, 276],[339, 276],[360, 280],[390, 290],
                    [422, 303],[447, 316],[467, 330],[485, 344],[496, 354],
                    [503, 363],[507, 371],[510, 376],[511, 384]
                ],
                "page": page
            }
        ]

        # Append each stroke to jsonList
        jsonList.extend(strokes)

    photos = render_strokes(jsonList, canvasH, canvasW)

    return send_file(
        photos,
        mimetype='application/pdf',
        as_attachment=True,
        download_name="canvas_export.pdf"
    )





