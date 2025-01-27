from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default="regular_user")  # 'admin' or 'regular_user'

    # New fields for user preferences
    profile_picture = db.Column(db.String(255), nullable=True)
    notification_email = db.Column(db.Boolean, default=True)  # Email notifications
    notification_in_app = db.Column(db.Boolean, default=True)  # In-app notifications
    dark_mode = db.Column(db.Boolean, default=False)  # Dark mode preference

    def set_password(self, password):
        """Sets the password hash for the user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def update_profile(self, data):
        """Updates user profile details."""
        self.username = data.get("username", self.username)
        self.email = data.get("email", self.email)
        self.name = data.get("name", self.name)
        self.profile_picture = data.get("profile_picture", self.profile_picture)

    def update_preferences(self, data):
        """Updates user notification and display preferences."""
        self.notification_email = data.get("notification_email", self.notification_email)
        self.notification_in_app = data.get("notification_in_app", self.notification_in_app)
        self.dark_mode = data.get("dark_mode", self.dark_mode)

    def to_dict(self):
        """Converts user information to a dictionary format."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "profile_picture": self.profile_picture,
            "notification_email": self.notification_email,
            "notification_in_app": self.notification_in_app,
            "dark_mode": self.dark_mode,
            "role": self.role,
        }
