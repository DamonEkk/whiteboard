from flask import Blueprint, render_template, jsonify, request, send_file
from io import BytesIO
from .users import generate_token, login_cognito, verify_token, confirm_cognito, signup_cognito
from .export import * 
import base64
import random
import boto3
import jwt

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

@main.route("/confirmation", methods=["GET"])
def sendConfirmation():
    username = request.args.get("username")
    return render_template("confirmation.html", username=username)


@main.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return jsonify({"error": "Missing fields"}), 400

    try:
        signup_cognito(username, password, email) # Call to users.py which calls and validates signup api
    except Exception as e:
        return jsonify({"Invalid signup"}), 400

    # calls confirmation html screen
    return ({"status": "signup worked", "username": username})

@main.route("/confirm", methods=["POST"])
def confirmation():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    code = data.get("code")
    username = data.get("username")
    
    confirm_cognito(code, username)

    return render_template("home.html")



@main.route("/users", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    try:
        token = login_cognito(username, password)
    except Exception as e:
        return jsonify({"error": "Incorrect credentials or user does not exist"}), 401


    decoded = jwt.decode(token, options={"verify_signature": False})
    groups = decoded.get("cognito:groups", [])
    if "Admin" in groups:
        role = "ADMIN"
    elif "Users" in groups:
        role = "USER"
    else:
        role = "GUEST"

    return jsonify({"token": token, "role": role})


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
    roomID = data.get("roomid")

    
    if len(strokes) == 0:
        print("Empty List", flush=True)

    photos = render_strokes(roomID, canvasH, canvasW)


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

    canvas = -6715537

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

        db = boto3.resource("dynamodb", region_name="ap-southeast-2")
        table = dunamodb.Table("n12197718-whiteboard-strokes")

        for stroke in strokes:
            table.put_item(
                Item = {
                    "roomid": canvas,
                    "strokenum": stroke.get("drawId"),
                    "stroke": stroke

                }
            )




    photos = render_strokes(canvas, canvasH, canvasW)

    return send_file(
        photos,
        mimetype='application/pdf',
        as_attachment=True,
        download_name="canvas_export.pdf"
    )

@main.route("/senddb", methods=["POST"])
def send_to_db():
    qutName = "n12197718@qut.edu.au"
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    stroke = data.get("stroke")
    roomID = data.get("roomid")
    strokenum = data.get("strokenum")

    db = boto3.resource("dynamodb", region_name="ap-southeast-2")
    table = db.Table("n12197718-whiteboard-strokes")

    table.put_item(
        Item={
            "qut-username": qutName,
            "roomID": str(roomID),
            "strokenum": str(strokenum),
            "points": stroke.get("points", []),
            "size": stroke.get("size"),
            "colour": stroke.get("colour"),
            "page": stroke.get("page")
        }
    )


    return jsonify({"status": "success"}), 200























