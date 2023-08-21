import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from flask_mail import Mail
from hangman.email_settings import MAIL_USERNAME, MAIL_PASSWORD


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://user:password@localhost:5455/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

from hangman.models.account import Account
from hangman.models.word import Word
from hangman.models.game_record import GameRecord

# from biudzetas.models import *

bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(account_id):
    db.create_all()
    return Account.query.get(int(account_id))


class AdminModelView(ModelView):
    def is_accessible(self):
        return (
            current_user.is_authenticated
            and current_user.email == "yakovsolo@gmail.com"
        )


from hangman.routes.account_routes import *
from hangman.routes.hangman_game_routes import *

admin = Admin(app)
admin.add_view(AdminModelView(Account, db.session))
admin.add_view(AdminModelView(Word, db.session))
admin.add_view(AdminModelView(GameRecord, db.session))

app.config["MAIL_SERVER"] = "smtp.rambler.ru"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
