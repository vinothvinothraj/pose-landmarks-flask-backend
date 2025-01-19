# pose_processor.py
import cv2
import mediapipe as mp
import numpy as np
import base64
import re
# Initialize MediaPipe Pose and Drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

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
        "shoulder": "No landmarks detected for shoulders",
        "angles": "No landmarks detected for angles",
        "overall_percentage": "No data available"
    }
    
    # Check for landmarks and evaluate conditions
    if results.pose_landmarks:
        # Get messages based on nose and shoulder conditions
        messages["nose"] = check_nose_position(results)
        messages["shoulder"] = get_shoulder_alignment_percentage(results)

         # Calculate angles and include them in messages
        angles = calculate_angles(results)
        messages["angles"] = angles

         # Calculate overall percentage and include it in messages
        overall_percentage = calculate_overall_percentage(results)
        messages["overall_percentage"] = overall_percentage

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

def get_shoulder_alignment_percentage(results):
    # Get shoulder angles from calculate_angles function
    angles = calculate_angles(results)
    left_shoulder_angle = angles["left_shoulder"]
    right_shoulder_angle = angles["right_shoulder"]
    
    # Define tolerance angle value
    tolerance_angle = 0
    
    # Analyze the angles
    if abs(left_shoulder_angle - right_shoulder_angle) <= tolerance_angle:
        return "Shoulders are aligned: 100%"
    else:
        alignment_percentage = max(0, 100 - abs(left_shoulder_angle - right_shoulder_angle))
        return f"Shoulders aligned: {alignment_percentage}%"

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    """
    a = np.array(a)  # first
    b = np.array(b)  # mid
    c = np.array(c)  # end

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return int(angle)

def calculate_angles(results):
    """
    Calculate angles for specific body parts using landmarks.
    """
    landmarks = results.pose_landmarks.landmark

    # Define key points for left and right sides
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

    nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
            landmarks[mp_pose.PoseLandmark.NOSE.value].y]

    # Calculate angles for shoulders
    left_shoulder_angle = calculate_angle(left_hip, left_shoulder, right_shoulder)
    right_shoulder_angle = calculate_angle(right_hip, right_shoulder, left_shoulder)

    # Calculate other angles (elbow and knee)
    l_elbow_angle = calculate_angle(left_hip, left_shoulder, left_wrist)
    l_knee_angle = calculate_angle(left_hip, left_knee, left_knee)
    r_elbow_angle = calculate_angle(right_hip, right_shoulder, right_wrist)
    r_knee_angle = calculate_angle(right_hip, right_knee, right_knee)
    head_angle = calculate_angle(left_shoulder, nose, right_shoulder)

    return {
        "left_shoulder": left_shoulder_angle,
        "right_shoulder": right_shoulder_angle,
        "left_elbow": l_elbow_angle,
        "left_knee": l_knee_angle,
        "right_elbow": r_elbow_angle,
        "right_knee": r_knee_angle,
    }


def extract_percentage(shoulder_string):
    # Use regular expression to find the percentage in the string
    match = re.search(r'(\d+)%', shoulder_string)
    if match:
        return int(match.group(1))
    return 0

def calculate_overall_percentage(results):
    shoulder_string = get_shoulder_alignment_percentage(results)  # Assume this returns a string with a percentage
    shoulder_score = extract_percentage(shoulder_string)  # Extract the numerical percentage

    # Calculate overall percentage (example logic)
    overall_percentage = shoulder_score
    return overall_percentage


    