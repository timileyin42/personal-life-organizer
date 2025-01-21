from flask import Blueprint, request, jsonify
from app.models.task import Task
from app.extensions import db

task_bp = Blueprint("task", __name__)

@task_bp.route("/", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(title=data["title"], due_date=data.get("due_date"))
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created successfully!"}), 201

@task_bp.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": task.id, "title": task.title, "due_date": task.due_date} for task in tasks]), 200

