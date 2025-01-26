from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.email import send_email
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime, timedelta

email_bp = Blueprint("email", __name__)

# Route to send a custom email notification
@email_bp.route("/send-notification", methods=["POST"])
@jwt_required()
def send_notification():
    """
    Send a custom email notification to a specific recipient.
    Request body must include 'subject', 'body', and optionally 'recipients'.
    """
    current_user = get_jwt_identity()
    data = request.get_json()

    subject = data.get("subject")
    body = data.get("body")
    recipients = data.get("recipients")  # Explicit recipients must be provided

    if not subject or not body:
        return jsonify({"error": "Subject and body are required."}), 400

    if not recipients or not isinstance(recipients, list):
        return jsonify({"error": "Recipients must be a list of email addresses."}), 400

    response = send_email(subject, recipients, body)

    if response["success"]:
        return jsonify({"message": "Notification sent successfully!"}), 200
    else:
        return jsonify({"error": response["message"]}), 500


# Automated reminder routes for overdue tasks and upcoming deadlines
@email_bp.route("/send-task-reminders", methods=["POST"])
@jwt_required()
def send_task_reminders():
    """
    Automatically send reminders for overdue tasks directly to task owners.
    """
    current_user = get_jwt_identity()
    current_user_email = current_user.get("email")  # Ensure email is part of the JWT payload
    current_date = datetime.now()

    # Fetch overdue tasks for the current user
    overdue_tasks = Task.query.filter_by(user_id=current_user.get("id"), completed=False).filter(
        Task.due_date < current_date
    ).all()

    if not overdue_tasks:
        return jsonify({"message": "No overdue tasks to remind."}), 200

    for task in overdue_tasks:
        recipient_email = task.user.email  # Assuming Task has a relationship with User
        subject = "Overdue Task Reminder"
        body = f"The following task is overdue: '{task.title}' (Due: {task.due_date.strftime('%Y-%m-%d')})"
        send_email(subject, [recipient_email], body)

    return jsonify({"message": "Task reminders sent successfully!"}), 200


@email_bp.route("/send-goal-deadline-reminders", methods=["POST"])
@jwt_required()
def send_goal_deadline_reminders():
    """
    Automatically notify goal setters about upcoming deadlines within the next 3 days.
    """
    current_user = get_jwt_identity()
    current_user_email = current_user.get("email")  # Ensure email is part of the JWT payload
    current_date = datetime.now()
    upcoming_date = current_date + timedelta(days=3)

    # Fetch goals with deadlines within the next 3 days for the current user
    upcoming_goals = Goal.query.filter_by(user_id=current_user.get("id")).filter(
        Goal.target_date >= current_date, Goal.target_date <= upcoming_date
    ).all()

    if not upcoming_goals:
        return jsonify({"message": "No upcoming goal deadlines to remind."}), 200

    for goal in upcoming_goals:
        recipient_email = goal.user.email  # Assuming Goal has a relationship with User
        subject = "Upcoming Goal Deadline Reminder"
        body = f"Your goal '{goal.title}' has a deadline approaching on {goal.target_date.strftime('%Y-%m-%d')}."
        send_email(subject, [recipient_email], body)

    return jsonify({"message": "Goal deadline reminders sent successfully!"}), 200

