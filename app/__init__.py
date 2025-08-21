from flask import Flask
from flask_socketio import SocketIO
from flask import render_template

app = None;

#boilerplate stuff

socketio = SocketIO()

# Factory pattern function that creates a modular flask app
def start_app():
    global app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev' #change key to something more private later
    socketio.init_app(app, cors_allowed_origins="*")

    # http routes from routes.py, registers them into blueprints making them more modular
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Moves socket logic into its own file for readability and modularity (idk if this is a word)
    from .sockets import socket_event_handler
    socket_event_handler(socketio)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html")

    @app.errorhandler(500)
    def internal(e):
        return render_template("500.html")

    return app

# initialise db here



