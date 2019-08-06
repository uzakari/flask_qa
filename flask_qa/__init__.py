from flask import Flask

from .extentions import login_manager, db, cors
from .commands import create_tables
from .models import User
from .routes.main import main
from .routes.auth import auth


def create_app(config_file='settings.py'):

    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    login_manager.init_app(app)

    db.init_app(app)
    
    cors.init_app(app)


    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.cli.add_command(create_tables)
    return app
