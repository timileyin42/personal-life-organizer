from flask import request
from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from app.logs.models import Log

def log_action(action, details=None):
    """
    Logs a user action to the database.
    :param action: The action being logged (string).
    :param details: Additional details to store (dictionary).
    """
    user_id = None
    try:
        user_id = get_jwt_identity()  # Get the logged-in user's ID
    except:
        pass  # Handle cases where no user is logged in (anonymous actions)

    log = Log(
        user_id=user_id,
        action=action,
        details=details or {},
    )
    db.session.add(log)
    db.session.commit()

