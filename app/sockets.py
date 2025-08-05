from flask_socketio import SocketIO, emit, disconnect, send
from flask import request

def socket_event_handler(socketio):

    @socketio.on('connect')
    def handle_connect():
        print("connection")
        # HERE is where we want to start the login process and establish that logic.
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"disconnected {request.sid}")
    
    @socketio.on('draw')
    def handle_draw():
        print("draw not ready")

    @socketio.on('colour')
    def handle_colour():
        print("colour not ready")

    @socketio.on('export')
    def handle_export():
        print("export not read")

