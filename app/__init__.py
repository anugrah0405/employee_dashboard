from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from app.utils.key_vault import MockKeyVault
from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    csrf = CSRFProtect(app)
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        from app.models import User
        User.create_default_user()
    
    return app