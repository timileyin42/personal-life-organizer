from app.extensions import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    target_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)

