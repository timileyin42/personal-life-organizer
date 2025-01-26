from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.goal import Goal
from app.logs.middleware import log_action
from app.utils.progress_utils import calculate_goal_progress, calculate_overall_progress
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the blueprint
goal_bp = Blueprint('goal', __name__)

# Create a new goal
@goal_bp.route("/", methods=["POST"])
@jwt_required()
def create_goal():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Validate required fields
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    try:
        new_goal = Goal(
            title=data["title"],
            description=data.get("description"),
            target_date=data.get("target_date"),
            priority=data.get("priority", "Medium"),
            user_id=current_user_id,
        )
        db.session.add(new_goal)
        db.session.commit()

        # Log the action
        log_action("create_goal", {"goal_id": new_goal.id, "title": new_goal.title})

        return jsonify({"message": "Goal created successfully!", "goal": new_goal.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to create goal: {str(e)}")  # Log the error
        return jsonify({"error": "Failed to create goal", "details": str(e)}), 500

# Retrieve goals
@goal_bp.route("/", methods=["GET"])
@jwt_required()
def get_goals():
    current_user_id = get_jwt_identity()

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Search and filter parameters
    search_query = request.args.get("search", "").lower()
    priority_filter = request.args.get("priority", "").capitalize()

    try:
        # Base query
        query = Goal.query.filter_by(user_id=current_user_id)

        # Apply search filter
        if search_query:
            query = query.filter(
                (Goal.title.ilike(f"%{search_query}%")) |
                (Goal.description.ilike(f"%{search_query}%"))
            )

        # Apply priority filter
        if priority_filter in ["Low", "Medium", "High"]:
            query = query.filter_by(priority=priority_filter)

        # Apply pagination
        pagination = query.paginate(page=page, per_page=per_page)
        goals = [goal.to_dict() for goal in pagination.items]

        return jsonify({
            "goals": goals,
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page
        }), 200
    except Exception as e:
        logger.error(f"Failed to retrieve goals: {str(e)}")  # Log the error
        return jsonify({"error": "Failed to retrieve goals", "details": str(e)}), 500

# Progress for a specific goal
@goal_bp.route("/<int:goal_id>/progress", methods=["GET"])
@jwt_required()
def get_goal_progress(goal_id):
    user_id = get_jwt_identity()

    # Check if goal exists and belongs to the user
    goal = Goal.query.filter_by(id=goal_id, user_id=user_id).first()
    if not goal:
        return jsonify({"error": "Goal not found or unauthorized"}), 404

    try:
        progress = calculate_goal_progress(goal_id)
        return jsonify({"goal_id": goal_id, "progress_percentage": progress}), 200
    except Exception as e:
        logger.error(f"Failed to get progress for goal {goal_id}: {str(e)}")  # Log the error
        return jsonify({"error": "Failed to retrieve goal progress", "details": str(e)}), 500

# Overall progress for all goals
@goal_bp.route("/progress", methods=["GET"])
@jwt_required()
def get_overall_progress():
    user_id = get_jwt_identity()
    try:
        progress = calculate_overall_progress(user_id)
        return jsonify({"user_id": user_id, "overall_progress_percentage": progress}), 200
    except Exception as e:
        logger.error(f"Failed to get overall progress for user {user_id}: {str(e)}")  # Log the error
        return jsonify({"error": "Failed to retrieve overall progress", "details": str(e)}), 500
