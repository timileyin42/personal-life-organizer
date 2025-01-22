from app.extensions import db
from datetime import datetime

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)  # Nullable for anonymous users
    action = db.Column(db.String(100), nullable=False)  # e.g., "create_goal", "update_task"
    details = db.Column(db.JSON, nullable=True)  # Store additional details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }

