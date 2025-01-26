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
    # Query parameters
    goal_id = request.args.get("goal_id", type=int)
    status_filter = request.args.get("status", "").lower()  # completed or pending
    search_query = request.args.get("search", "").lower()

    try:
        # Base query
        query = Task.query

        # Filter by goal_id
        if goal_id:
            query = query.filter_by(goal_id=goal_id)

        # Apply status filter
        if status_filter == "completed":
            query = query.filter_by(completed=True)
        elif status_filter == "pending":
            query = query.filter_by(completed=False)

        # Apply search filter
        if search_query:
            query = query.filter(Task.title.ilike(f"%{search_query}%"))

        # Fetch tasks
        tasks = [task.to_dict() for task in query.all()]
        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve tasks", "details": str(e)}), 500

