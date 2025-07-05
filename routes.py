from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth_bp', __name__)

USERNAME = "admin"
PASSWORD = "password123"

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == USERNAME and data['password'] == PASSWORD:
        return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid credentials"}), 401
