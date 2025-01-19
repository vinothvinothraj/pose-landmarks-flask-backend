# app.py
from flask import Flask
from flask_socketio import SocketIO, emit
from pose_processor import process_pose_image  # Import the processing function
from config import Config
from models import init_db, db
from models.user import User
from models.session import Session
from flask_migrate import Migrate
from routes import init_routes
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and migrations
init_db(app)
migrate = Migrate(app, db)

# Initialize routes
init_routes(app)

# Enable CORS globally for the Flask app
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('frame')
def handle_frame(data):
    # Process the frame using the function from pose_processor.py
    frame_encoded, messages = process_pose_image(data)
    
    # Emit the processed frame and individual messages for each landmark to the client
    emit('processed_frame', {
        'image': frame_encoded,
        'nose_message': messages["nose"],
        'shoulder_message': messages["shoulder"],
        'angles': messages["angles"],
        'overall_percentage': messages["overall_percentage"],
        'head_horizontal_message': messages["head_horizontal"],  
        'head_horizontal_percentage': messages["head_horizontal_percentage"]

    })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
