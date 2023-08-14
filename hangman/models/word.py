from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy import DateTime
from datetime import datetime
from itsdangerous import Serializer
from flask_login import UserMixin
from sqlalchemy.sql import func

from hangman import app, db


class Word(db.Model, UserMixin):
    __tablename__ = "words"
    id = db.Column(Integer, primary_key=True, index=True)
    word = db.Column(String, unique=True, nullable=False)
    word_length = db.Column(Integer, nullable=False)
    category = db.Column(String, nullable=False)
    times_called = db.Column(Integer, default=0)
    times_answered = db.Column(Integer, default=0)
    times_lost = db.Column(Integer, default=0)
