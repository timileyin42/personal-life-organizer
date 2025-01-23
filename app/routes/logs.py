from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.logs.models import Log
from app.extensions import db
from app.utils.decorators import admin_required

log_bp = Blueprint('log', __name__)

@log_bp.route("/", methods=["GET"])
@jwt_required()
def get_logs():
    # Pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Query logs with pagination
    logs = Log.query.paginate(page=page, per_page=per_page)

    # Convert log objects to dictionaries
    log_data = [{
        "id": log.id,
        "action": log.action,
        "details": log.details,
        "timestamp": log.timestamp
    } for log in logs.items]

    return jsonify({
        "logs": log_data,
        "total": logs.total,
        "page": logs.page,
        "pages": logs.pages
    }), 200

