from flask import Blueprint, render_template

# The file is all about routing traffic to the correct urls


main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/canvas")
def canvas():
    return render_template("canvas.html")
