from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Ajout de Flask-Migrate

db = SQLAlchemy()
migrate = Migrate()  # Ajout de Migrate
login_manager = LoginManager()
login_manager.login_view = "main.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)  # Initialiser Flask-Migrate
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main
    app.register_blueprint(main)

    return app
