from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.models.goal import Goal
from app.models.user import User  # Assuming User model is needed for points and streaks
from app.extensions import db
from datetime import datetime

# Blueprint for task routes
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

@task_bp.route("/<int:task_id>", methods=["PATCH"])
@jwt_required()
def complete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if task.completed:
        return jsonify({"message": "Task already completed"}), 400

    # Mark task as completed
    task.completed = True
    task.completed_date = datetime.utcnow()

    # Get the user from the JWT
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if task was completed before the deadline
    if task.due_date and task.completed_date < task.due_date:
        user.points = user.points + 10  # Award 10 points for early completion

    # Update streak if the user has completed tasks consecutively
    last_task = Task.query.filter_by(user_id=user_id, completed=True).order_by(Task.completed_date.desc()).first()
    if last_task and (task.completed_date - last_task.completed_date).days == 1:
        user.streak = user.streak + 1  # Increase streak count
    else:
        user.streak = 1  # Reset streak if not consecutive

    db.session.commit()
    return jsonify({
        "message": "Task completed successfully!",
        "task": task.to_dict(),
        "points": user.points,
        "streak": user.streak
    }), 200

