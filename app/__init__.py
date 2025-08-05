from flask import flask
from flask_socketio import SocketIO

#boilerplate stuff

socketio = SocketIO()

# Factory pattern function that creates a modular flask app
def start_app():
    app = Flask(__name__)
    app.config['SECRET'] = 'dev' #change key to something more private later
    socketio.init_app(app, cors_allowed_origins="*")

    # http routes from routes.py, registers them into blueprints making them more modular
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Moves socket logic into its own file for readability and modularity (idk if this is a word)
    from .sockets import register_socketio_events
    register_socketio_events(socketio)

    return app

