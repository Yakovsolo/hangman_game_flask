import os
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, logout_user, login_user, login_required


# from PIL import Image
from flask_mail import Message, Mail
from hangman import db, app, bcrypt, mail
from hangman.forms.hangman_game_forms import GamePlayForm, GameStartForm
from hangman.models.account import Account
from game import HangmanGame
from database_crud import GameRecordCrud


@app.route("/history", methods=["GET"])
@login_required
def history():
    user_id = current_user.id  # Получаем ID текущего пользователя
    game_record_crud = GameRecordCrud(db=db.session)  # Создаем экземпляр GameRecordCrud
    user_games = game_record_crud.get_game_records_by_account_id(
        user_id
    )  # Получаем игры пользователя

    return render_template("history.html", user_games=user_games)


@app.route("/start_game", methods=["GET", "POST"])
@login_required
def start_game():
    form = GameStartForm()

    # Очистка данных из сессии
    session.pop("game_id", None)
    session.pop("used_letters", None)
    session.pop("hashed_word", None)
    session.pop("image_name", "Default")
    session.pop("wrong_attempts", 0)

    if form.validate_on_submit():
        category = form.category.data
        difficulty = form.difficulty.data

        game = HangmanGame(
            db=db.session,
            game_settings=None,
        )

        game_settings = game.get_game_settings(category=category, difficulty=difficulty)
        db_word = game.get_random_word(game_settings)
        category = db_word.category
        word = db_word.word
        word_length = db_word.word_length
        game_result = "In Progress"
        account_id = current_user.id

        game_info_id = game.create_game_record(
            category=category,
            word=word,
            word_length=word_length,
            game_result=game_result,
            account_id=account_id,
        )
        session["game_info_id"] = game_info_id
        return redirect(url_for("play_game"))
    return render_template("start_game.html", form=form)


@app.route("/play_game", methods=["GET", "POST"])
@login_required
def play_game():
    form = GamePlayForm()
    game_info_id = session.get("game_info_id")

    if game_info_id is None:
        return redirect(url_for("start_game"))

    game = HangmanGame(
        db=db.session,
        game_settings=None,
    )

    game_info = game.get_game_record_by_id(game_info_id)
    word = game_info.word

    hashed_word = session.get("hashed_word", game.hash_word(word))

    used_letters = session.get("used_letters", [])
    wrong_attempts = session.get("wrong_attempts", 0)
    image_name = session.get("image_name", "Default")
    result = ""

    if request.method == "POST":
        new_letter = request.form.get("letter").upper()

        if new_letter in used_letters:
            flash("You have already used this letter.", "danger")
        else:
            used_letters.append(new_letter)
            session["used_letters"] = used_letters
            hashed_word = game.try_letter(new_letter, word, hashed_word)
            session["hashed_word"] = hashed_word
            if hashed_word == word:
                result = "WIN"
                game.update_game_record(game_info_id, result)
                return render_template("win.html")

            if new_letter not in word:
                wrong_attempts += 1
                print(image_name)
                image_name = "Hangman" + str(wrong_attempts)
                print(image_name)
                session["wrong_attempts"] = wrong_attempts
                session["image_name"] = image_name
                if wrong_attempts == 10:
                    result = "LOST"
                    game.update_game_record(game_info_id, result)
                    return render_template("lose.html")

    return render_template(
        "play_game.html",
        hashed_word=hashed_word,
        result=result,
        used_letters=used_letters,
        wrong_attempts=wrong_attempts,
        image_name=image_name,
        form=form,
    )


@app.route("/exit", methods=["POST"])
def exit():
    session.clear()
    return redirect("/play_game")  # Перенаправьте пользователя на главную страницу
