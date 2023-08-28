from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Boolean, DateTime, Integer, String

from hangman import db


class GameRecord(db.Model, UserMixin):
    __tablename__ = "game_records"
    id = db.Column(Integer, primary_key=True)
    game_date = db.Column(DateTime, default=datetime.now)
    category = db.Column(String, nullable=False)
    word = db.Column(String, nullable=False)
    word_length = db.Column(Integer, nullable=False)
    game_result = db.Column(Boolean, default=False)
    account_id = db.Column(Integer, db.ForeignKey("accounts.id"))
    account = db.relationship("Account", back_populates="game_record")
