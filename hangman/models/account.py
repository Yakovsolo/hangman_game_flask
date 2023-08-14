from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy import DateTime
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from sqlalchemy.sql import func
from hangman import app, db


class Account(db.Model, UserMixin):
    __tablename__ = "accounts"
    id = db.Column(Integer, primary_key=True, index=True)
    name = db.Column(String, nullable=False)
    surname = db.Column(String, nullable=False)
    email = db.Column(String, unique=True, index=True)
    password = db.Column(String(60), nullable=False)
    registration_date = db.Column(DateTime, default=datetime.now())
    avatar = db.Column(String(20), nullable=False, default="default.jpg")
    games_played = db.Column(Integer)
    games_win = db.Column(Integer)
    games_loose = db.Column(Integer)
    game_record = db.relationship("GameRecord")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])

        try:
            account_id = s.loads(token)["user_id"]
        except:
            return None
        return Account.query.get(account_id)
