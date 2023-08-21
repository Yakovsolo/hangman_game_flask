from typing import List, Optional


from sqlalchemy.orm import Session

from hangman import app, db

from typing import Any, Dict

from hangman.models.word import Word

from random import choice

from database_crud import GameRecordCrud, WordCrud, AccountCrud


class HangmanGame(GameRecordCrud, WordCrud, AccountCrud):
    def __init__(self, db: Session, game_settings: Dict[str, Any]) -> None:
        super().__init__(db)  # Initialize inherited CRUD classes
        self.game_settings = game_settings

    def get_game_settings(self, category, difficulty):
        if difficulty == "Easy":
            game_settings = {
                "category": category,
                "min_length": 2,
                "max_length": 5,
            }
            return game_settings
        elif difficulty == "Medium":
            game_settings = {
                "category": category,
                "min_length": 5,
                "max_length": 7,
            }
            return game_settings
        elif difficulty == "Hard":
            game_settings = {
                "category": category,
                "min_length": 7,
                "max_length": 100,
            }
            return game_settings

    def hash_word(self, word: str) -> str:
        hashed_word_list = []
        for char in word:
            if char.isalpha():
                hashed_word_list.append("_")
            elif char == "-":
                hashed_word_list.append("-")
            elif char == " ":
                hashed_word_list.append(" ")
        return "".join(hashed_word_list)

    def try_letter(self, letter: str, word: str, hashed_word):
        if letter in word:
            for index, char in enumerate(word):
                if char == letter:
                    new_hashed_word = list(hashed_word)
                    new_hashed_word[index] = letter
                    hashed_word = "".join(new_hashed_word)
            return hashed_word
        else:
            return hashed_word


if __name__ == "__main__":
    with app.app_context():
        game_settings = {
            "category": "space",
            "min_length": 7,
            "max_length": 100,
        }

        game = HangmanGame(
            db=db.session,  # Используем db.session
            game_settings=game_settings,
        )

        db_word = game.get_random_word(
            category="space",
            min_length=7,
            max_length=100,
        )
        word = db_word.word
        print(word)

        hashed_word = game.hash_word(db_word)
        print(hashed_word)
        counter = 10
        while counter > 0:
            new_letter = input("Please enter letter").upper()
            hashed_word = game.try_letter(new_letter, word, hashed_word)
            print(hashed_word)
            print(str(counter))
            counter -= 1
            if hashed_word == word:
                print("You win")
                break
        if hashed_word != word:
            print(str(counter))
