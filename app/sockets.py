from flask_socketio import SocketIO, emit, disconnect, send
from flask import request

def socket_event_handler(socketio):

    @socketio.on('draw')
    def handle_draw():
        print("draw not ready")

    @socketio.on('colour')
    def handle_colour():
        print("colour not ready")


    @socketio.on('sync-canvas')
    def handle_sync_canvas():
        print("sync")

    @socketio.on('clear-canvas')
    def handle_clear_canvas():
        print("clearing canvas")
        # needs to clear canvas for all and clear history array
    
    @socketio.on('undo-canvas')
    def handle_undo():
        print("undoing")
        # Needs to clear canvas and redraw global history except client (who undid) history[-1]

    @socketio.on('mouse-movement')
    def handle_user_mouse():
        print("moving")
        # Gets a .json of user name, room, x and y and displays pointer to other users every 50-100ms
