from flask import Blueprint, request, jsonify
from models import db
from models.user import User

# Define a Blueprint for user routes
user_bp = Blueprint('user_routes', __name__)

# Create a user
@user_bp.route('/users', methods=['POST'])
def create_user():
    print("Creating user", request.json)
    data = request.json
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({"error": "Name and age are required"}), 400

    user = User(name=name, age=age)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user": {"id": user.id, "name": user.name, "age": user.age}}), 201

# Get all users
@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "name": user.name, "age": user.age} for user in users]
    return jsonify({"users": user_list}), 200

# Delete a user by ID
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User with ID {user_id} deleted successfully"}), 200


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Return user details as JSON
    return jsonify({"id": user.id, "name": user.name, "age": user.age}), 200
