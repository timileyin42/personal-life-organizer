from app.extensions import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    reminder_time = db.Column(db.DateTime, nullable=True)
    notified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)  # Link to a Goal

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "completed": self.completed,
            "reminder_time": self.reminder_time,
            "notified": self.notified,
            "created_at": self.created_at,
            "goal_id": self.goal_id
        }

