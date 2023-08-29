import os
import unittest

from hangman import app, db
from hangman.game import HangmanGame


class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        os.environ["FLASK_ENV"] = "testing"
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_game_settings(self):
        game = HangmanGame(db.session, None)
        game_settings = game.get_game_settings("animals", "Easy")
        self.assertEqual(game_settings["category"], "animals")
        self.assertEqual(game_settings["min_length"], 2)
        self.assertEqual(game_settings["max_length"], 5)

    def test_hash_word(self):
        game = HangmanGame(db.session, None)
        hashed_word = game.hash_word("HELLO")
        self.assertEqual(hashed_word, "_____")

    def test_try_letter_correct(self):
        game = HangmanGame(db.session, None)
        new_hashed_word = game.try_letter("L", "HELLO", "_____")
        self.assertEqual(new_hashed_word, "__LL_")

    def test_try_letter_incorrect(self):
        game = HangmanGame(db.session, None)
        new_hashed_word = game.try_letter("Z", "HELLO", "_____")
        self.assertEqual(new_hashed_word, "_____")
