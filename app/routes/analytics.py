from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.logs.services import get_logs_by_user, get_recent_logs, get_action_count

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

