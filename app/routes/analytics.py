from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.logs.services import get_logs_by_user, get_recent_logs, get_action_count
from datetime import datetime, timedelta
from app.extensions import db
from app.models.goal import Goal
from app.models.task import Task

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")

@analytics_bp.route("/user", methods=["GET"])
@jwt_required()
def user_logs():
    """
    Fetch logs for the current user.
    """
    user_id = get_jwt_identity()
    logs = get_logs_by_user(user_id)
    return jsonify([log.to_dict() for log in logs]), 200

@analytics_bp.route("/recent", methods=["GET"])
def recent_logs():
    """
    Fetch recent logs across all users.
    """
    logs = get_recent_logs()
    return jsonify([log.to_dict() for log in logs]), 200

@analytics_bp.route("/count/<action>", methods=["GET"])
def action_count(action):
    """
    Fetch the count of a specific action.
    """
    count = get_action_count(action)
    return jsonify({"action": action, "count": count}), 200

@analytics_bp.route("/reports/weekly", methods=["GET"])
@jwt_required()
def weekly_report():
    current_user_id = get_jwt_identity()
    now = datetime.utcnow()
    one_week_ago = now - timedelta(days=7)

    # Fetch goals and tasks from the past week
    weekly_goals = Goal.query.filter(
        Goal.user_id == current_user_id,
        Goal.created_at >= one_week_ago
    ).all()

    weekly_tasks = Task.query.filter(
        Task.due_date >= one_week_ago
    ).all()

    # Calculate completed goals and tasks
    completed_goals = [goal for goal in weekly_goals if goal.completed]
    completed_tasks = [task for task in weekly_tasks if task.completed]

    # Prepare statistics
    stats = {
        "total_goals": len(weekly_goals),
        "completed_goals": len(completed_goals),
        "total_tasks": len(weekly_tasks),
        "completed_tasks": len(completed_tasks),
        "goal_completion_percentage": round(len(completed_goals) / len(weekly_goals) * 100, 2) if weekly_goals else 0,
        "task_completion_percentage": round(len(completed_tasks) / len(weekly_tasks) * 100, 2) if weekly_tasks else 0,
    }

    return jsonify({"message": "Weekly report generated successfully", "stats": stats}), 200

@analytics_bp.route("/reports/monthly", methods=["GET"])
@jwt_required()
def monthly_report():
    current_user_id = get_jwt_identity()
    now = datetime.utcnow()
    one_month_ago = now - timedelta(days=30)

    # Fetch goals and tasks from the past month
    monthly_goals = Goal.query.filter(
        Goal.user_id == current_user_id,
        Goal.created_at >= one_month_ago
    ).all()

    monthly_tasks = Task.query.filter(
        Task.due_date >= one_month_ago
    ).all()

    # Calculate completed goals and tasks
    completed_goals = [goal for goal in monthly_goals if goal.completed]
    completed_tasks = [task for task in monthly_tasks if task.completed]

    # Prepare statistics
    stats = {
        "total_goals": len(monthly_goals),
        "completed_goals": len(completed_goals),
        "total_tasks": len(monthly_tasks),
        "completed_tasks": len(completed_tasks),
        "goal_completion_percentage": round(len(completed_goals) / len(monthly_goals) * 100, 2) if monthly_goals else 0,
        "task_completion_percentage": round(len(completed_tasks) / len(monthly_tasks) * 100, 2) if monthly_tasks else 0,
    }

    return jsonify({"message": "Monthly report generated successfully", "stats": stats}), 200


@analytics_bp.route("/reports/yearly", methods=["GET"])
@jwt_required()
def yearly_report():
    current_user_id = get_jwt_identity()
    now = datetime.utcnow()
    one_year_ago = now - timedelta(days=365)

    # Fetch goals and tasks from the past year
    yearly_goals = Goal.query.filter(
        Goal.user_id == current_user_id,
        Goal.created_at >= one_year_ago
    ).all()

    yearly_tasks = Task.query.filter(
        Task.due_date >= one_year_ago
    ).all()

    # Calculate completed goals and tasks
    completed_goals = [goal for goal in yearly_goals if goal.completed]
    completed_tasks = [task for task in yearly_tasks if task.completed]

    # Prepare statistics
    stats = {
        "total_goals": len(yearly_goals),
        "completed_goals": len(completed_goals),
        "total_tasks": len(yearly_tasks),
        "completed_tasks": len(completed_tasks),
        "goal_completion_percentage": round(len(completed_goals) / len(yearly_goals) * 100, 2) if yearly_goals else 0,
        "task_completion_percentage": round(len(completed_tasks) / len(yearly_tasks) * 100, 2) if yearly_tasks else 0,
    }

    return jsonify({"message": "Yearly report generated successfully", "stats": stats}), 200

