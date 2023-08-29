import logging
import logging.config
from os import path
from typing import Any, Dict

from sqlalchemy.orm import Session

from hangman import app, db
from hangman.database_crud import AccountCrud, GameRecordCrud, WordCrud

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")


class HangmanGame(GameRecordCrud, WordCrud, AccountCrud):
    def __init__(self, db: Session, game_settings: Dict[str, Any]) -> None:
        super().__init__(db)
        self.game_settings = game_settings

    def get_game_settings(
        self,
        category: str,
        difficulty: str,
    ) -> Dict[str, Any]:
        try:
            if difficulty == "Easy":
                game_settings = {
                    "category": category,
                    "min_length": 2,
                    "max_length": 5,
                }
            elif difficulty == "Medium":
                game_settings = {
                    "category": category,
                    "min_length": 5,
                    "max_length": 7,
                }
            elif difficulty == "Hard":
                game_settings = {
                    "category": category,
                    "min_length": 7,
                    "max_length": 100,
                }
            else:
                raise ValueError("Invalid difficulty level")

            return game_settings

        except Exception as e:
            logger.error(f"An error occurred while getting game settings: {e}")
            return {}

    def hash_word(
        self,
        word: str,
    ) -> str:
        try:
            hashed_word_list = []
            for char in word:
                if char.isalpha():
                    hashed_word_list.append("_")
                elif char == "-":
                    hashed_word_list.append("-")
                elif char == " ":
                    hashed_word_list.append(" ")
            return "".join(hashed_word_list)

        except Exception as e:
            logger.error(f"An error occurred while hashing word: {e}")
            return ""

    def try_letter(
        self,
        letter: str,
        word: str,
        hashed_word: str,
    ) -> str:
        try:
            if letter in word:
                new_hashed_word = list(hashed_word)
                for index, char in enumerate(word):
                    if char == letter:
                        new_hashed_word[index] = letter
                return "".join(new_hashed_word)
            else:
                return hashed_word

        except Exception as e:
            logger.error(f"An error occurred while trying letter: {e}")
            return hashed_word


if __name__ == "__main__":
    with app.app_context():
        game_settings = {
            "category": "space",
            "min_length": 7,
            "max_length": 100,
        }

        game = HangmanGame(
            db=db.session,
            game_settings=game_settings,
        )

        db_word = game.get_random_word(
            category="space",
            min_length=7,
            max_length=100,
        )
        word = db_word.word

        hashed_word = game.hash_word(db_word)
        counter = 10
        while counter > 0:
            new_letter = input("Please enter letter").upper()
            hashed_word = game.try_letter(new_letter, word, hashed_word)
            counter -= 1
            if hashed_word == word:
                print("You win")
                break
        if hashed_word != word:
            print(hashed_word)
