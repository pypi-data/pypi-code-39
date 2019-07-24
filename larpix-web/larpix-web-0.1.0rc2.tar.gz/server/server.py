from .app import create_app, socketio

app = create_app()
socketio.run(app, port=5000)

