from app.logs.models import Log

def get_logs_by_user(user_id, limit=50):
    """
    Fetch logs for a specific user.
    """
    return Log.query.filter_by(user_id=user_id).order_by(Log.timestamp.desc()).limit(limit).all()

def get_action_count(action):
    """
    Get the count of a specific action.
    """
    return Log.query.filter_by(action=action).count()

def get_recent_logs(limit=50):
    """
    Fetch the most recent logs across all users.
    """
    return Log.query.order_by(Log.timestamp.desc()).limit(limit).all()

