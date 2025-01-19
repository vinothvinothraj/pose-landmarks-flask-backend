from flask import Blueprint, request, jsonify
from models import db
from models.session import Session
from datetime import datetime

# Define a Blueprint for session routes
session_bp = Blueprint('session_routes', __name__)

# Create a session
@session_bp.route('/sessions', methods=['POST'])
def create_session():
    data = request.json

    session_name = data.get('session_name')
    user_id = data.get('user_id')
    posture_type = data.get('posture_type')
    start_time = data.get('start_time', datetime.utcnow())  # Default to current time
    end_time = data.get('end_time')
    avg_good_posture = data.get('avg_good_posture')
    avg_bad_posture = data.get('avg_bad_posture')
    session_posture_score = data.get('session_posture_score')

    if not session_name or not posture_type:
        return jsonify({"error": "Session name and posture type are required"}), 400

    session = Session(
        session_name=session_name,
        user_id=user_id,
        posture_type=posture_type,
        start_time=start_time,
        end_time=end_time,
        avg_good_posture=avg_good_posture,
        avg_bad_posture=avg_bad_posture,
        session_posture_score=session_posture_score
    )
    db.session.add(session)
    db.session.commit()
    return jsonify({"message": "Session created successfully", "session": {
        "id": session.id,
        "session_name": session.session_name,
        "user_id": session.user_id,
        "posture_type": session.posture_type,
        "start_time": session.start_time,
        "end_time": session.end_time,
        "avg_good_posture": session.avg_good_posture,
        "avg_bad_posture": session.avg_bad_posture,
        "session_posture_score": session.session_posture_score
    }}), 201

# Get all sessions
@session_bp.route('/sessions', methods=['GET'])
def get_sessions():
    sessions = Session.query.all()
    session_list = [{
        "id": session.id,
        "session_name": session.session_name,
        "user_id": session.user_id,
        "posture_type": session.posture_type,
        "start_time": session.start_time,
        "end_time": session.end_time,
        "avg_good_posture": session.avg_good_posture,
        "avg_bad_posture": session.avg_bad_posture,
        "session_posture_score": session.session_posture_score
    } for session in sessions]
    return jsonify({"sessions": session_list}), 200

# Delete a session by ID
@session_bp.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    db.session.delete(session)
    db.session.commit()
    return jsonify({"message": f"Session with ID {session_id} deleted successfully"}), 200


# Get all sessions for a given user_id
@session_bp.route('/sessions/user/<int:user_id>', methods=['GET'])
def get_sessions_by_user(user_id):
    sessions = Session.query.filter_by(user_id=user_id).all()
    if not sessions:
        return jsonify({"message": f"No sessions found for user_id {user_id}"}), 404

    session_list = [{
        "id": session.id,
        "session_name": session.session_name,
        "user_id": session.user_id,
        "posture_type": session.posture_type,
        "start_time": session.start_time,
        "end_time": session.end_time,
        "avg_good_posture": session.avg_good_posture,
        "avg_bad_posture": session.avg_bad_posture,
        "session_posture_score": session.session_posture_score
    } for session in sessions]
    
    return jsonify({"user_id": user_id, "sessions": session_list}), 200
