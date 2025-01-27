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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)  # Link to a Goal

    # New fields for sharing
    shared_with = db.Column(db.String(255), nullable=True)  # Comma-separated user IDs or usernames
    permission_level = db.Column(db.String(20), default="view")  # 'view' or 'edit'

    comments = db.relationship("Comment", backref="task", lazy=True)  # New relationship for comments

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "completed": self.completed,
            "reminder_time": self.reminder_time,
            "notified": self.notified,
            "created_at": self.created_at,
            "goal_id": self.goal_id,
            "shared_with": self.shared_with,
            "user_id": self.user_id,
            "permission_level": self.permission_level
        }
