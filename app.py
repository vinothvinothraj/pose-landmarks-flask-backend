# app.py
from flask import Flask
from flask_socketio import SocketIO, emit
from pose_processor import process_pose_image  # Import the processing function

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('frame')
def handle_frame(data):
    # Process the frame using the function from pose_processor.py
    frame_encoded, messages = process_pose_image(data)
    
    # Emit the processed frame and individual messages for each landmark to the client
    emit('processed_frame', {
        'image': frame_encoded,
        'nose_message': messages["nose"],
        'shoulder_message': messages["shoulder"]
    })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
