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
    

@app.route('/video_player')
def video_player():
    return render_template('video_player.html')    

from flask import jsonify  # Add this import at the top if not already present
import random  # Ensure the random module is imported

@app.route('/graph_data')
def graph_data():
    """
    Returns JSON data for a line graph with 100 data points.
    Each data point is a random float between 0 and 5.
    
    Returns:
        JSON: {
            "labels": [1, 2, ..., 100],
            "values": [random_value1, random_value2, ..., random_value100]
        }
    """
    data = {
        'labels': list(range(1, 101)),
        'values': [round(random.uniform(0, 5), 2) for _ in range(100)]
    }
    return jsonify(data)

if __name__ == '__main__':
    socketio.run(app, debug=True)