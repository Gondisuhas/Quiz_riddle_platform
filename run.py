"""Entry point. Starts the Flask app with Socket.IO on http://127.0.0.1:5000."""
from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == "__main__":
    # Flask-SocketIO 5.x without eventlet/gevent -> threaded async mode (dev OK).
    socketio.run(app, host="127.0.0.1", port=5000, debug=False, allow_unsafe_werkzeug=True)
