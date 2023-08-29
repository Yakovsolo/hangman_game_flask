import logging
import logging.config
from os import path
from random import choice
from typing import List, Optional

from sqlalchemy.orm import Session

from hangman.models.account import Account
from hangman.models.game_record import GameRecord
from hangman.models.word import Word

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")


class AccountCrud:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create_account(
        self,
        name: str,
        surname: str,
        email: str,
        password: str,
        avatar: str = "default.jpg",
    ) -> Optional[Account]:
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
        try:
            self.db.add(new_account)
            self.db.commit()
            logger.info(f"Created account with ID: {new_account.id}")
            return new_account

        except Exception as e:
            self.db.rollback()
            logger.error(f"An error occurred while creating an account: {e}")
            return None

    def get_account_by_id(
        self,
        account_id: int,
    ) -> Optional[Account]:
        try:
            return self.db.query(Account).filter_by(id=account_id).first()

        except Exception as e:
            logger.error(f"An error occurred while fetching an account: {e}")
            return None

    def get_all_account_statistic(self) -> List[Account]:
        try:
            return (
                self.db.query(Account)
                .filter(Account.is_admin == False)
                .order_by(Account.games_win.desc())
                .all()
            )

        except Exception as e:
            logger.error(f"An error occurred while fetching account statistics: {e}")
            return []

    def update_account_stats(
        self,
        account: Account,
        games_played: int,
        games_win: int,
        games_loose: int,
    ) -> Optional[Account]:
        try:
            account.games_played = games_played
            account.games_win = games_win
            account.games_loose = games_loose
            self.db.commit()
            return account

        except Exception as e:
            logger.error(f"An error occurred while updating account stats: {e}")
            return None

    def update_account_data(
        self,
        account: Account,
        name: str,
        surname: str,
        email: str,
        avatar: str,
    ) -> Optional[Account]:
        try:
            account.name = name
            account.surname = surname
            account.email = email
            account.avatar = avatar
            self.db.commit()
            return account

        except Exception as e:
            logger.error(f"An error occurred while updating account data: {e}")
            return None

    def delete_account(
        self,
        account: Account,
    ) -> None:
        try:
            self.db.delete(account)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting an account: {e}")


class GameRecordCrud:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create_game_record(
        self,
        category: str,
        word: str,
        word_length: int,
        account_id: int,
    ) -> Optional[int]:
        game_record = GameRecord(
            category=category,
            word=word,
            word_length=word_length,
            account_id=account_id,
        )
        try:
            self.db.add(game_record)
            self.db.commit()
            logger.info(f"Created game record with ID: {game_record.id}")
            return game_record.id

        except Exception as e:
            self.db.rollback()
            logger.error(f"An error occurred while creating a game record: {e}")
            return None

    def get_game_record_by_id(
        self,
        record_id: int,
    ) -> Optional[GameRecord]:
        try:
            record = self.db.query(GameRecord).filter_by(id=record_id).first()
            if record is None:
                logger.warning(f"Game record with id {record_id} not found")
            return record

        except Exception as e:
            logger.error(f"An error occurred while fetching game record: {e}")
            return None

    def get_game_records_by_account_id(
        self,
        account_id: int,
    ) -> Optional[List[GameRecord]]:
        try:
            records = self.db.query(GameRecord).filter_by(account_id=account_id).all()
            return records

        except Exception as e:
            logger.error(
                f"An error occurred while fetching game records by account id: {e}"
            )
            return None

    def get_all_game_records(self) -> Optional[List[GameRecord]]:
        try:
            records = self.db.query(GameRecord).all()
            return records

        except Exception as e:
            logger.error(f"An error occurred while fetching all game records: {e}")
            return None

    def update_game_record(
        self,
        game_id: int,
        new_result: bool,
    ) -> Optional[GameRecord]:
        try:
            game_record = self.get_game_record_by_id(game_id)
            if game_record:
                game_record.game_result = new_result
                self.db.commit()
                return game_record
            else:
                logger.warning(f"Game record with id {game_id} not found")
                return None

        except Exception as e:
            logger.error(f"An error occurred while updating game record: {e}")
            return None


class WordCrud:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create_word(
        self,
        word: str,
        word_length: int,
        category: str,
    ) -> Optional[Word]:
        try:
            new_word = Word(
                word=word,
                word_length=word_length,
                category=category,
            )
            self.db.add(new_word)
            self.db.commit()
            return new_word

        except Exception as e:
            logger.error(f"An error occurred while creating word: {e}")
            return None

    def get_word_by_word(
        self,
        word: str,
    ) -> Optional[Word]:
        try:
            word = word.upper()
            return self.db.query(Word).filter_by(word=word).first()

        except Exception as e:
            logger.error(f"An error occurred while fetching word: {e}")
            return None

    def get_random_word(
        self,
        game_settings: dict,
    ) -> Optional[Word]:
        try:
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

        except Exception as e:
            logger.error(f"An error occurred while fetching random word: {e}")
            return None

    def get_all_words(self) -> List[Word]:
        try:
            return self.db.query(Word).order_by(Word.id).all()

        except Exception as e:
            logger.error(f"An error occurred while fetching all words: {e}")
            return []

    def update_word_stats(
        self,
        word: Word,
        times_called: int,
        times_answered: int,
        times_lost: int,
    ) -> Optional[Word]:
        try:
            word.times_called = times_called
            word.times_answered = times_answered
            word.times_lost = times_lost
            self.db.commit()
            return word

        except Exception as e:
            logger.error(f"An error occurred while updating word stats: {e}")
            return None

    def delete_word(
        self,
        word: str,
    ) -> None:
        try:
            self.db.delete(word)
            self.db.commit()

        except Exception as e:
            logger.error(f"An error occurred while deleting word: {e}")
