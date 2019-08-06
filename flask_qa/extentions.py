from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS, cross_origin

login_manager = LoginManager()

db =  SQLAlchemy()

cors = CORS()



