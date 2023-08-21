from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy import DateTime
from datetime import datetime
from itsdangerous import Serializer
from flask_login import UserMixin
from sqlalchemy.sql import func
from hangman import app, db


class GameRecord(db.Model, UserMixin):
    __tablename__ = "game_records"
    id = db.Column(Integer, primary_key=True)
    game_date = db.Column(DateTime, default=datetime.now())
    category = db.Column(String, nullable=False)
    word = db.Column(String, nullable=False)
    word_length = db.Column(Integer, nullable=False)
    game_result = db.Column(String, nullable=False)
    account_id = db.Column(Integer, db.ForeignKey("accounts.id"))
