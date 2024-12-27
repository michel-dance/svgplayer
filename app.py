import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/websocket')
def websocket():
    return render_template('websocket.html')

@socketio.on('connect')
def handle_connect():
    def send_svg():
        while True:
            svg_payload = '<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" /></svg>'
            socketio.emit('svg', svg_payload)
            socketio.sleep(5)
    
    socketio.start_background_task(send_svg)

if __name__ == '__main__':
    socketio.run(app, debug=True)