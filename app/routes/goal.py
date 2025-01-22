from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.goal import Goal

# Define the blueprint
goal_bp = Blueprint('goal', __name__)

# Protect all routes
@goal_bp.route("/", methods=["POST"])
@jwt_required()
def create_goal():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    new_goal = Goal(
        title=data["title"],
        description=data.get("description"),
        target_date=data.get("target_date"),
        priority=data.get("priority", "Medium"),
        user_id=current_user_id,
    )
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"message": "Goal created successfully!", "goal": new_goal.to_dict()}), 201

@goal_bp.route("/", methods=["GET"])
@jwt_required()
def get_goals():
    current_user_id = get_jwt_identity()
    goals = Goal.query.filter_by(user_id=current_user_id).all()
    return jsonify([goal.to_dict() for goal in goals]), 200

