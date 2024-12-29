import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')
thread_lock = Lock()

# Dictionary to keep track of client states
client_states = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/websocket')
def websocket():
    return render_template('websocket.html')

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    client_states[client_id] = {'paused': False}
    print(f'Client connected: {client_id}')

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    client_states.pop(client_id, None)
    print(f'Client disconnected: {client_id}')

@socketio.on('play_svg_video', namespace='/video')
def handle_play_svg_video():
    client_id = request.sid
    if client_id not in client_states:
        client_states[client_id] = {}
    client_states[client_id]['paused'] = False

    if 'second' not in client_states[client_id]:
        client_states[client_id]['second'] = 0

    print('handle_play_svg_video')
    socketio.start_background_task(send_svg_video, client_id)

@socketio.on('pause_svg_video', namespace='/video')
def handle_pause_svg_video():
    client_id = request.sid
    client_states[client_id]['paused'] = True
    print('handle_pause_svg_video')

def send_svg_video(client_id):
    print('send_svg_video')
    total_seconds = 100
    svg_width = 500
    radius = 40
    second = client_states[client_id]['second']
    while second < (total_seconds):
        if client_states.get(client_id, {}).get('paused', False):
            print(f'Playback paused for client: {client_id}')
            break  # Exit the loop if paused

        # Calculate the x position based on the current second
        x_position = (svg_width - radius * 2) * second / total_seconds + radius
        svg_payload = (
            f'<svg width="{svg_width}" height="100">'
            f'<circle cx="{x_position}" cy="50" r="{radius}" stroke="black" stroke-width="3" fill="blue" />'
            f'</svg>'
        )
        socketio.emit('svg_frame', svg_payload, namespace='/video', room=client_id)
        socketio.sleep(1)  # Wait for 1 second before sending the next frame

        # Update the second for the client
        client_states[client_id]['second'] = second
        second += 1
    

if __name__ == '__main__':
    socketio.run(app, debug=True)