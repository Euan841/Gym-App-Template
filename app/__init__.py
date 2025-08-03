import os
from flask import Flask

from . import db

def create_app():
    app = Flask(__name__)
    # Database file stored at project root
    app.config['DATABASE'] = os.path.join(app.root_path, '..', 'data.db')

    # Initialize database and register teardown
    db.init_app(app)

    # Register blueprints
    from .main import main_bp
    app.register_blueprint(main_bp)

    # Ensure the database and tables exist
    with app.app_context():
        db.init_db()

    return app
