from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.milestone import Milestone
from app.models.goal import Goal
from app.extensions import db

milestone_bp = Blueprint("milestone", __name__)

# Add a milestone to a goal
@milestone_bp.route("/<int:goal_id>/milestones", methods=["POST"])
@jwt_required()
def add_milestone(goal_id):
    user_id = get_jwt_identity()
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    
    if not goal:
        return jsonify({"error": "Goal not found or unauthorized"}), 404
    
    data = request.get_json()
    new_milestone = Milestone(
        title=data["title"],
        description=data.get("description"),
        target_date=data.get("target_date"),
        goal_id=goal.id
    )
    db.session.add(new_milestone)
    db.session.commit()
    
    return jsonify({"message": "Milestone added successfully!", "milestone": new_milestone.to_dict()}), 201

# View milestones for a goal
@milestone_bp.route("/<int:goal_id>/milestones", methods=["GET"])
@jwt_required()
def get_milestones(goal_id):
    user_id = get_jwt_identity()
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    
    if not goal:
        return jsonify({"error": "Goal not found or unauthorized"}), 404

    milestones = Milestone.query.filter_by(goal_id=goal.id).all()
    return jsonify([milestone.to_dict() for milestone in milestones]), 200

# Update a milestone or mark it as completed
@milestone_bp.route("/milestones/<int:milestone_id>", methods=["PUT"])
@jwt_required()
def update_milestone(milestone_id):
    user_id = get_jwt_identity()
    milestone = Milestone.query.join(Goal).filter(
        Milestone.id == milestone_id, Goal.user_id == user_id
    ).first()
    
    if not milestone:
        return jsonify({"error": "Milestone not found or unauthorized"}), 404
    
    data = request.get_json()
    milestone.title = data.get("title", milestone.title)
    milestone.description = data.get("description", milestone.description)
    milestone.target_date = data.get("target_date", milestone.target_date)
    milestone.completed = data.get("completed", milestone.completed)
    db.session.commit()
    
    return jsonify({"message": "Milestone updated successfully!", "milestone": milestone.to_dict()}), 200

