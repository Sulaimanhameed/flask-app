from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config
import time
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    """Application factory function"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp)

    # Initialize database with retry logic
    with app.app_context():
        max_retries = 5
        for attempt in range(max_retries):
            try:
                db.create_all()
                app.logger.info("Database tables created successfully")
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    app.logger.error(f"Failed to create tables after {max_retries} attempts: {str(e)}")
                    raise
                app.logger.warning(f"Database initialization failed (attempt {attempt + 1}), retrying...")
                time.sleep(2)
                db.session.remove()

    return app
