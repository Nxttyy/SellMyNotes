from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdb.db"

db = SQLAlchemy()
db.init_app(app)

bcrypt = Bcrypt(app)


login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

login_manager.init_app(app)


# app.add_url_rule('/node_modules', endpoint='filename',
#                  view_func=app.send_static_file)