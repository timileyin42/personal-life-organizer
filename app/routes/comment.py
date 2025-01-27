from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.comment import Comment
from app.models.task import Task
from app.models.goal import Goal
from app.extensions import db

# Define the blueprint for comments
comment_bp = Blueprint('comment', __name__)

# Add a comment to a task
@comment_bp.route("/task/<int:task_id>", methods=["POST"])
@jwt_required()
def add_task_comment(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get("content"):
        return jsonify({"error": "Comment content is required"}), 400

    # Check if the task exists
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Create a new comment
    new_comment = Comment(
        content=data["content"],
        user_id=user_id,
        task_id=task_id
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully!", "comment": new_comment.to_dict()}), 201

# Add a comment to a goal
@comment_bp.route("/goal/<int:goal_id>", methods=["POST"])
@jwt_required()
def add_goal_comment(goal_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or not data.get("content"):
        return jsonify({"error": "Comment content is required"}), 400

    # Check if the goal exists
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify({"error": "Goal not found"}), 404

    # Create a new comment
    new_comment = Comment(
        content=data["content"],
        user_id=user_id,
        goal_id=goal_id
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"message": "Comment added successfully!", "comment": new_comment.to_dict()}), 201

# Get comments for a task
@comment_bp.route("/task/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task_comments(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    comments = Comment.query.filter_by(task_id=task_id).all()
    return jsonify({"comments": [comment.to_dict() for comment in comments]}), 200

# Get comments for a goal
@comment_bp.route("/goal/<int:goal_id>", methods=["GET"])
@jwt_required()
def get_goal_comments(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify({"error": "Goal not found"}), 404

    comments = Comment.query.filter_by(goal_id=goal_id).all()
    return jsonify({"comments": [comment.to_dict() for comment in comments]}), 200

# Delete a comment
@comment_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    # Check if the user is the owner of the comment
    if comment.user_id != user_id:
        return jsonify({"error": "Unauthorized to delete this comment"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted successfully!"}), 200
