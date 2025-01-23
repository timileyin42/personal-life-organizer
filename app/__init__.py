from flask import Flask
from .extensions import db, migrate, jwt
from .routes.auth import auth_bp
from .routes.task import task_bp
from .routes.goal import goal_bp
from .routes.logs import log_bp

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object("app.config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(task_bp, url_prefix="/tasks")
    app.register_blueprint(goal_bp, url_prefix="/auth/goals")
    app.register_blueprint(log_bp, url_prefix="/logs")


    return app
