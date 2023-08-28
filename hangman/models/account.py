import logging
import logging.config
from datetime import datetime
from os import path

from flask_login import UserMixin
from itsdangerous import Serializer
from sqlalchemy import Boolean, DateTime, Integer, String

from hangman import app, db

log_file_path = path.join(path.dirname(path.abspath(__file__)), "../logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")


class Account(db.Model, UserMixin):
    __tablename__ = "accounts"
    id = db.Column(Integer, primary_key=True, index=True)
    name = db.Column(String, nullable=False)
    surname = db.Column(String, nullable=False)
    email = db.Column(String, unique=True, index=True)
    password = db.Column(String(60), nullable=False)
    registration_date = db.Column(DateTime, default=datetime.now())
    avatar = db.Column(String(20), nullable=False, default="default.jpg")
    games_played = db.Column(Integer, default=0)
    games_win = db.Column(Integer, default=0)
    games_loose = db.Column(Integer, default=0)
    is_admin = db.Column(Boolean, default=False, nullable=False)
    game_record = db.relationship("GameRecord", back_populates="account")

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

    def reset_password(self, new_password):
        from hangman import bcrypt

        hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
        self.password = hashed_password
        db.session.commit()

    @classmethod
    def create_admin(cls, name, surname, email, password):
        from hangman import bcrypt

        try:
            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            admin_account = cls(
                name=name,
                surname=surname,
                email=email,
                password=hashed_password,
                is_admin=True,
            )
            db.session.add(admin_account)
            db.session.commit()
            logger.info("Admin account created successfully")
            return admin_account
        except Exception as e:
            db.session.rollback()
            logger.error(f"An error occurred while creating an admin account: {e}")
            return None
