from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from notesproject.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from notesproject.users.routes import users
    from notesproject.main.routes import main
    from notesproject.upload.routes import upload
    from notesproject.create.routes import create
    from notesproject.view.routes import view
    from notesproject.study.routes import study
    from notesproject.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(upload)
    app.register_blueprint(create)
    app.register_blueprint(view)
    app.register_blueprint(study)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
