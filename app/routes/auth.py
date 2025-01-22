from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

# User registration
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    # Check if the user already exists
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "User  already exists"}), 400

    # Create a new user
    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    
    # Add the user to the database
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User  registered successfully!"}), 201

# User login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    # Find the user by email
    user = User.query.filter_by(email=data["email"]).first()

    # Check if the user exists and the password is correct
    if user and user.check_password(data["password"]):
        # Create access token with user ID as a string
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401

# User profile
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    # Get the current user's identity from the JWT
    current_user_id = get_jwt_identity()
    
    # Retrieve the user from the database
    user = User.query.get(current_user_id)
    
    # Return user information as JSON
    return jsonify(user.to_dict()), 200
