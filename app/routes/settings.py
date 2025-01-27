from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User

settings_bp = Blueprint("settings", __name__)

# Update profile information
@settings_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.profile_picture = data.get("profile_picture", user.profile_picture)

    db.session.commit()
    return jsonify({"message": "Profile updated successfully", "user": user.to_dict()}), 200


# Change password
@settings_bp.route("/password", methods=["PUT"])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verify current password
    if not check_password_hash(user.password, data.get("current_password")):
        return jsonify({"error": "Current password is incorrect"}), 400

    # Update password
    user.password = generate_password_hash(data["new_password"])
    db.session.commit()
    return jsonify({"message": "Password changed successfully"}), 200


# Update notification preferences
@settings_bp.route("/preferences", methods=["PUT"])
@jwt_required()
def update_preferences():
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.notification_email = data.get("notification_email", user.notification_email)
    user.notification_in_app = data.get("notification_in_app", user.notification_in_app)
    user.dark_mode = data.get("dark_mode", user.dark_mode)

    db.session.commit()
    return jsonify({"message": "Preferences updated successfully"}), 200


# Get preferences
@settings_bp.route("/preferences", methods=["GET"])
@jwt_required()
def get_preferences():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    preferences = {
        "notification_email": user.notification_email,
        "notification_in_app": user.notification_in_app,
        "dark_mode": user.dark_mode,
    }
    return jsonify({"preferences": preferences}), 200

