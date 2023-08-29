import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from hangman.config import config
from hangman.email_settings import MAIL_PASSWORD, MAIL_USERNAME

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(24)

app.config.from_object(config[os.environ.get("FLASK_ENV", "default")])

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

from hangman.models.account import Account
from hangman.models.game_record import GameRecord
from hangman.models.word import Word

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD

bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(account_id):
    db.create_all()
    return Account.query.get(int(account_id))


from hangman.routes.account_routes import *
from hangman.routes.hangman_game_routes import *
