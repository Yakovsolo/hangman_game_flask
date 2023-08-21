from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Session
from hangman.models.game_record import GameRecord
from hangman.models.word import Word
from hangman.models.account import Account
from hangman import db
from random import choice


class GameRecordCrud:
    def __init__(self, db: Session):
        self.db = db

    def create_game_record(self, category, word, word_length, game_result, account_id):
        game_record = GameRecord(
            category=category,
            word=word,
            word_length=word_length,
            game_result=game_result,
            account_id=account_id,
        )
        self.db.add(game_record)
        self.db.commit()
        return game_record.id

    def get_game_record_by_id(self, record_id):
        return self.db.query(GameRecord).filter_by(id=record_id).first()

    def get_game_records_by_account_id(self, account_id):
        return self.db.query(GameRecord).filter_by(account_id=account_id).all()

    def get_all_game_records(self):
        return self.db.query(GameRecord).all()

    def update_game_record(self, game_id, new_result):
        game_record = self.get_game_record_by_id(game_id)
        game_record.game_result = new_result
        self.db.commit()
        return game_record

    def delete_game_record(self, game_record):
        self.db.delete(game_record)
        self.db.commit()

    def as_dict(self):
        return {
            "id": self.id,
            "game_date": self.game_date,
            "category": self.category,
            "word": self.word,
            "word_length": self.word_length,
            "game_result": self.game_result,
            "account_id": self.account_id,
        }


class WordCrud:
    def __init__(self, db: Session):
        self.db = db

    def create_word(self, word, word_length, category):
        new_word = Word(word=word, word_length=word_length, category=category)
        self.db.add(new_word)
        self.db.commit()
        return new_word

    def get_word_by_id(self, word_id):
        return self.db.query(Word).filter_by(id=word_id).first()

    def get_random_word(self, game_settings):
        print(game_settings)
        words = (
            self.db.query(Word)
            .filter(
                Word.category == game_settings["category"],
                Word.word_length >= game_settings["min_length"],
                Word.word_length < game_settings["max_length"],
            )
            .all()
        )
        word = choice(words)
        return word

    def get_all_words(self):
        return self.db.query(Word).all()

    def update_word_stats(self, word, times_called, times_answered, times_lost):
        word.times_called = times_called
        word.times_answered = times_answered
        word.times_lost = times_lost
        self.db.commit()
        return word

    def delete_word(self, word):
        self.db.delete(word)
        self.db.commit()


class AccountCrud:
    def __init__(self, db: Session):
        self.db = db

    def create_account(self, name, surname, email, password, avatar="default.jpg"):
        new_account = Account(
            name=name,
            surname=surname,
            email=email,
            password=password,
            avatar=avatar,
            games_played=0,
            games_win=0,
            games_loose=0,
        )
        self.db.add(new_account)
        self.db.commit()
        return new_account

    def get_account_by_id(self, account_id):
        return self.db.query(Account).filter_by(id=account_id).first()

    def get_account_by_email(self, email):
        return self.db.query(Account).filter_by(email=email).first()

    def update_account_stats(self, account, games_played, games_win, games_loose):
        account.games_played = games_played
        account.games_win = games_win
        account.games_loose = games_loose
        self.db.commit()
        return account

    def delete_account(self, account):
        self.db.delete(account)
        self.db.commit()
