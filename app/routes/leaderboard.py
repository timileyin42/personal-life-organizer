from flask import Blueprint, jsonify
from app.models.user import User

leaderboard_bp = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")

@leaderboard_bp.route("/", methods=["GET"])
def get_leaderboard():
    top_users = User.query.order_by(User.points.desc()).limit(10).all()
    leaderboard = [{"username": user.username, "points": user.points} for user in top_users]
    return jsonify(leaderboard), 200

