# pose_processor.py
import cv2
import mediapipe as mp
import numpy as np
import base64

# Initialize MediaPipe Pose and Drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def process_pose_image(image_data):
    """
    Process the input image data with MediaPipe Pose detection and return
    the processed image in base64 encoding along with individual messages.
    """
    # Decode the image from base64
    np_image = np.frombuffer(base64.b64decode(image_data), np.uint8)
    frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    # Process the frame with MediaPipe Pose
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    messages = {
        "nose": "No landmarks detected for nose",
        "shoulder": "No landmarks detected for shoulders"
    }
    
    # Check for landmarks and evaluate conditions
    if results.pose_landmarks:
        # Get messages based on nose and shoulder conditions
        messages["nose"] = check_nose_position(results)
        messages["shoulder"] = check_shoulder_position(results)

        # Draw landmarks on the frame if detected
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
        )

    # Encode the processed frame to base64
    _, buffer = cv2.imencode('.jpg', frame)
    frame_encoded = base64.b64encode(buffer).decode('utf-8')
    
    return frame_encoded, messages

def check_nose_position(results):
    """
    Check the Y-coordinate of the nose landmark to determine head position.
    """
    nose_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
    if nose_y < 0.3:
        return "Head is raised"
    elif nose_y > 0.7:
        return "Head is lowered"
    else:
        return "Head is in a neutral position"

def check_shoulder_position(results):
    """
    Check the relative position of the shoulders to detect slouching or upright posture.
    """
    left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
    right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
    
    # Compare shoulder positions to check for symmetry (example condition)
    if abs(left_shoulder - right_shoulder) > 0.1:
        return "Shoulders are not level"
    else:
        return "Shoulders are level"

