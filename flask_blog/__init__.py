from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = r"\xebr\x17D*t\xae\xd4\xe3S\xb6\xe2\xebP1\x8b"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_blog import routes
