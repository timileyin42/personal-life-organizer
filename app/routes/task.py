from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.models.goal import Goal
from app.extensions import db

task_bp = Blueprint("task", __name__)

@task_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json()
    goal_id = data.get("goal_id")

    # Check if goal exists
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify({"error": "Goal not found"}), 404

    new_task = Task(
        title=data["title"],
        due_date=data.get("due_date"),
        goal_id=goal_id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created successfully!", "task": new_task.to_dict()}), 201

@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    goal_id = request.args.get("goal_id")
    if goal_id:
        tasks = Task.query.filter_by(goal_id=goal_id).all()
    else:
        tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

