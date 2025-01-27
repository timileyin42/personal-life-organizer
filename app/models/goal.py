from app.extensions import db
from datetime import datetime

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    target_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), default="Medium")  # Low, Medium, High
    completed = db.Column(db.Boolean, default=False)
    reminder_time = db.Column(db.DateTime, nullable=True)
    notified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # New fields for sharing
    shared_with = db.Column(db.String(255), nullable=True)  # Comma-separated user IDs or usernames
    permission_level = db.Column(db.String(20), default="view")  # 'view' or 'edit'

    # Relationship with tasks
    tasks = db.relationship('Task', backref='goal', cascade='all, delete-orphan', lazy=True)
    milestones = db.relationship("Milestone", backref="goal", lazy=True)
    comments = db.relationship("Comment", backref="goal", lazy=True)  # New relationship for comments

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "target_date": self.target_date,
            "priority": self.priority,
            "completed": self.completed,
            "reminder_time": self.reminder_time,
            "notified": self.notified,
            "created_at": self.created_at,
            "tasks": [task.to_dict() for task in self.tasks],
            "shared_with": self.shared_with,
            "permission_level": self.permission_level
        }
