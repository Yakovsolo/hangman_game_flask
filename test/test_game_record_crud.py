import os
import unittest

from hangman import app, db
from hangman.database_crud import AccountCrud, GameRecordCrud, WordCrud
from hangman.models.game_record import GameRecord


class TestAccountCrud(unittest.TestCase):
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

    def test_create_account(self):
        crud = AccountCrud(db.session)

        new_account = crud.create_account("John", "Doe", "john@example.com", "password")

        self.assertIsNotNone(new_account)
        self.assertEqual(new_account.name, "John")
        self.assertEqual(new_account.surname, "Doe")
        self.assertEqual(new_account.email, "john@example.com")
        self.assertEqual(new_account.password, "password")

    def test_get_account_by_id(self):
        crud = AccountCrud(db.session)
        new_account = crud.create_account("John", "Doe", "john@example.com", "password")

        retrieved_account = crud.get_account_by_id(new_account.id)

        self.assertIsNotNone(retrieved_account)
        self.assertEqual(retrieved_account.name, "John")
        self.assertEqual(retrieved_account.surname, "Doe")
        self.assertEqual(retrieved_account.email, "john@example.com")
        self.assertEqual(retrieved_account.password, "password")

    def test_update_account_stats(self):
        crud = AccountCrud(db.session)

        new_account = crud.create_account("John", "Doe", "john@example.com", "password")
        updated_account = crud.update_account_stats(
            new_account, games_played=10, games_win=5, games_loose=5
        )

        self.assertIsNotNone(updated_account)
        self.assertEqual(updated_account.games_played, 10)
        self.assertEqual(updated_account.games_win, 5)
        self.assertEqual(updated_account.games_loose, 5)

    def test_get_all_account_statistic(self):
        crud = AccountCrud(db.session)
        first_account = crud.create_account(
            "John",
            "Doe",
            "john@example.com",
            "password",
        )
        second_account = crud.create_account(
            name="Jane",
            surname="Smith",
            email="jane@example.com",
            password="password",
        )
        crud.update_account_stats(
            first_account, games_played=10, games_win=5, games_loose=5
        )
        crud.update_account_stats(
            second_account, games_played=10, games_win=8, games_loose=2
        )

        accounts_statistic = crud.get_all_account_statistic()
        self.assertEqual(len(accounts_statistic), 2)
        self.assertEqual(accounts_statistic[0].name, "Jane")
        self.assertEqual(accounts_statistic[1].name, "John")

    def test_update_account_data(self):
        crud = AccountCrud(db.session)
        new_account = crud.create_account("John", "Doe", "john@example.com", "password")

        updated_account = crud.update_account_data(
            new_account,
            name="Updated",
            surname="Surname",
            email="updated@example.com",
            avatar="avatar.jpg",
        )

        self.assertIsNotNone(updated_account)
        self.assertEqual(updated_account.name, "Updated")
        self.assertEqual(updated_account.surname, "Surname")
        self.assertEqual(updated_account.email, "updated@example.com")
        self.assertEqual(updated_account.avatar, "avatar.jpg")

    def test_delete_account(self):
        crud = AccountCrud(db.session)
        new_account = crud.create_account("John", "Doe", "john@example.com", "password")

        crud.delete_account(new_account)
        deleted_account = crud.get_account_by_id(new_account.id)
        self.assertIsNone(deleted_account)

    def test_create_game_record(self):
        account_crud = AccountCrud(db.session)
        new_account = account_crud.create_account(
            "John", "Doe", "john@example.com", "password"
        )

        game_record_crud = GameRecordCrud(db.session)
        result_id = game_record_crud.create_game_record(
            "animals", "DOG", 3, new_account.id
        )

        self.assertIsNotNone(result_id)

        created_record = db.session.get(GameRecord, result_id)
        self.assertEqual(created_record.category, "animals")
        self.assertEqual(created_record.word, "DOG")
        self.assertEqual(created_record.word_length, 3)
        self.assertEqual(created_record.account_id, new_account.id)

    def test_get_game_record_by_id(self):
        account_crud = AccountCrud(db.session)
        new_account = account_crud.create_account(
            "John", "Doe", "john@example.com", "password"
        )

        game_record_crud = GameRecordCrud(db.session)
        result_id = game_record_crud.create_game_record(
            "animals", "DOG", 3, new_account.id
        )

        retrieved_record = game_record_crud.get_game_record_by_id(result_id)

        self.assertIsNotNone(retrieved_record)
        self.assertEqual(retrieved_record.category, "animals")
        self.assertEqual(retrieved_record.word, "DOG")
        self.assertEqual(retrieved_record.word_length, 3)
        self.assertEqual(retrieved_record.account_id, new_account.id)

    def test_get_game_records_by_account_id(self):
        account_crud = AccountCrud(db.session)
        new_account = account_crud.create_account(
            "John", "Doe", "john@example.com", "password"
        )

        game_record_crud = GameRecordCrud(db.session)
        game_record_crud.create_game_record("animals", "DOG", 3, new_account.id)
        game_record_crud.create_game_record("cities", "VILNIUS", 7, new_account.id)
        retrieved_records = game_record_crud.get_game_records_by_account_id(
            new_account.id
        )

        self.assertIsNotNone(retrieved_records)
        self.assertEqual(len(retrieved_records), 2)

    def test_get_all_game_records(self):
        account_crud = AccountCrud(db.session)
        game_record_crud = GameRecordCrud(db.session)

        new_account = account_crud.create_account(
            "John", "Doe", "john@example.com", "password"
        )

        game_record_crud.create_game_record("animals", "DOG", 3, new_account.id)
        game_record_crud.create_game_record("cities", "VILNIUS", 7, new_account.id)
        game_record_crud.create_game_record("mountains", "PUTORANA", 8, new_account.id)

        all_records = game_record_crud.get_all_game_records()

        self.assertIsNotNone(all_records)
        self.assertEqual(len(all_records), 3)

        self.assertEqual(all_records[0].category, "animals")
        self.assertEqual(all_records[0].word, "DOG")
        self.assertEqual(all_records[0].word_length, 3)

        self.assertEqual(all_records[1].category, "cities")
        self.assertEqual(all_records[1].word, "VILNIUS")
        self.assertEqual(all_records[1].word_length, 7)

        self.assertEqual(all_records[2].category, "mountains")
        self.assertEqual(all_records[2].word, "PUTORANA")
        self.assertEqual(all_records[2].word_length, 8)

    def test_update_game_record(self):
        account_crud = AccountCrud(db.session)
        game_record_crud = GameRecordCrud(db.session)

        new_account = account_crud.create_account(
            "John", "Doe", "john@example.com", "password"
        )
        game_record_id = game_record_crud.create_game_record(
            "animals", "DOG", 3, new_account.id
        )

        updated_record = game_record_crud.update_game_record(game_record_id, True)

        self.assertIsNotNone(updated_record)
        self.assertEqual(updated_record.game_result, True)
        invalid_record_id = game_record_id + 100
        result = game_record_crud.update_game_record(invalid_record_id, False)
        self.assertIsNone(result)

    def test_create_word(self):
        crud = WordCrud(db.session)
        new_word = crud.create_word("DOG", 3, "animals")

        self.assertIsNotNone(new_word)
        self.assertEqual(new_word.word, "DOG")
        self.assertEqual(new_word.word_length, 3)
        self.assertEqual(new_word.category, "animals")

    def test_get_word_by_word(self):
        crud = WordCrud(db.session)
        new_word = crud.create_word("DOG", 3, "animals")
        retrieved_word = crud.get_word_by_word("dog")

        self.assertIsNotNone(retrieved_word)
        self.assertEqual(retrieved_word.word, "DOG")
        self.assertEqual(retrieved_word.word_length, 3)
        self.assertEqual(retrieved_word.category, "animals")

    def test_update_word_stats(self):
        crud = WordCrud(db.session)
        new_word = crud.create_word("DOG", 3, "animals")

        updated_word = crud.update_word_stats(new_word, 5, 3, 2)

        self.assertIsNotNone(updated_word)
        self.assertEqual(updated_word.times_called, 5)
        self.assertEqual(updated_word.times_answered, 3)
        self.assertEqual(updated_word.times_lost, 2)

    def test_delete_word(self):
        crud = WordCrud(db.session)
        word = crud.create_word("DOG", 3, "animals")

        deleted_word = crud.delete_word(word)
        self.assertIsNone(deleted_word)

    def test_get_random_word(self):
        crud = WordCrud(db.session)
        first_word = crud.create_word("OCELOT", 6, "animals")
        second_word = crud.create_word("LEMUR", 5, "animals")
        third_word = crud.create_word("SPOON", 5, "home")
        fourth_word = crud.create_word("TABLE", 5, "home")

        game_settings = {
            "category": "animals",
            "min_length": 5,
            "max_length": 7,
        }
        random_word = crud.get_random_word(game_settings)

        self.assertIsNotNone(random_word)
        self.assertTrue(random_word.category in game_settings["category"])
        self.assertTrue(
            game_settings["min_length"]
            <= random_word.word_length
            < game_settings["max_length"]
        )
