from app import start_app, socketio

app = start_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)
