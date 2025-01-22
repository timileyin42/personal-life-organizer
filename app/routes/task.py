from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.task import Task
from flask_jwt_extended import jwt_required, get_jwt_identity

task_bp = Blueprint("task", __name__)

# Create a new task
@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json()
    new_task = Task(
        title=data["title"],
        description=data.get("description"),
        status=data.get("status", "pending"),
        due_date=data.get("due_date"),
        goal_id=data["goal_id"]
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

# Get all tasks for a specific goal
@task_bp.route("/goals/<int:goal_id>/tasks", methods=["GET"])
@jwt_required()
def get_tasks(goal_id):
    tasks = Task.query.filter_by(goal_id=goal_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

# Update a task
@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    task.due_date = data.get("due_date", task.due_date)
    db.session.commit()
    return jsonify(task.to_dict()), 200

# Delete a task
@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"}), 204
