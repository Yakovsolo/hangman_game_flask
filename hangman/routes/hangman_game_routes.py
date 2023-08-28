import logging
import logging.config
from os import path

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from hangman import app, db
from hangman.database_crud import AccountCrud, GameRecordCrud
from hangman.forms.hangman_game_forms import GamePlayForm, GameStartForm
from hangman.forms.word_forms import AddWordForm, DeleteWordForm
from hangman.game import HangmanGame
from hangman.routes.account_routes import admin_required

log_file_path = path.join(path.dirname(path.abspath(__file__)), "../logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")


@app.route("/rules")
def rules():
    return render_template("rules.html")


@app.route("/history", methods=["GET"])
@login_required
def history():
    user_id = current_user.id
    game_record_crud = GameRecordCrud(db=db.session)
    user_games = game_record_crud.get_game_records_by_account_id(user_id)

    if user_games is None:
        flash("No game records found.", "info")
        logger.info("No game records found.")
        return render_template("history.html", user_games=[])

    return render_template("history.html", user_games=user_games)


@app.route("/statistics", methods=["GET"])
@login_required
def statistics():
    accounts = AccountCrud(db=db.session)
    account_stats = accounts.get_all_account_statistic()
    if account_stats is None:
        flash("No game statistics found.", "info")
        logger.info("No game statistics found.")
        return render_template("statistics.html", accounts=[])

    return render_template("statistics.html", accounts=account_stats)


@app.route("/start_game", methods=["GET", "POST"])
@login_required
def start_game():
    form = GameStartForm()
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
        account_id = current_user.id

        game_info_id = game.create_game_record(
            category=category,
            word=word,
            word_length=word_length,
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
    image_name = session.get("image_name", "default")
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
                result = True
                game.update_account_stats(
                    current_user,
                    current_user.games_played + 1,
                    current_user.games_win + 1,
                    current_user.games_loose,
                )
                db_word = game.get_word_by_word(word)
                game.update_word_stats(
                    db_word,
                    db_word.times_called + 1,
                    db_word.times_answered + 1,
                    db_word.times_lost,
                )
                game.update_game_record(game_info_id, result)
                user_id = current_user.id
                account = game.get_account_by_id(user_id)
                logger.info(f"Player with ID {user_id} won the game.")
                return render_template("win.html", account=account, word=word)

            if new_letter not in word:
                wrong_attempts += 1
                image_name = "hangman" + str(wrong_attempts)
                session["wrong_attempts"] = wrong_attempts
                session["image_name"] = image_name

                if wrong_attempts == 10:
                    result = False
                    game.update_game_record(game_info_id, result)
                    game.update_account_stats(
                        current_user,
                        current_user.games_played + 1,
                        current_user.games_win,
                        current_user.games_loose + 1,
                    )
                    db_word = game.get_word_by_word(word)
                    game.update_word_stats(
                        db_word,
                        db_word.times_called + 1,
                        db_word.times_answered,
                        db_word.times_lost + 1,
                    )
                    game.update_game_record(game_info_id, result)
                    user_id = current_user.id
                    account = game.get_account_by_id(user_id)
                    logger.info(
                        f"Game ID {game_info_id} ended in win. User: {current_user.id}, Word: {word}"
                    )
                    return render_template("lose.html", account=account, word=word)

    return render_template(
        "play_game.html",
        hashed_word=hashed_word,
        result=result,
        used_letters=used_letters,
        wrong_attempts=wrong_attempts,
        image_name=image_name,
        form=form,
    )


@app.route("/restart_and_record_loss", methods=["POST"])
@login_required
def restart_and_record_loss():
    game_info_id = session.get("game_info_id")

    if game_info_id is not None:
        game = HangmanGame(
            db=db.session,
            game_settings=None,
        )
        game_record = game.get_game_record_by_id(game_info_id)
        word = game_record.word

        game.update_game_record(game_info_id, False)
        game.update_account_stats(
            current_user,
            current_user.games_played + 1,
            current_user.games_win,
            current_user.games_loose + 1,
        )
        db_word = game.get_word_by_word(word)
        game.update_word_stats(
            db_word,
            db_word.times_called + 1,
            db_word.times_answered,
            db_word.times_lost + 1,
        )

        logger.info(
            f"Game ID {game_info_id} ended in loss. User: {current_user.id}, Word: {word}"
        )

    session.pop("game_info_id", None)
    session.pop("hashed_word", None)
    session.pop("used_letters", None)
    session.pop("wrong_attempts", None)
    return redirect(url_for("play_game"))


@app.route("/record_loss", methods=["POST"])
@login_required
def record_loss():
    game_info_id = session.get("game_info_id")

    if game_info_id is not None:
        game = HangmanGame(
            db=db.session,
            game_settings=None,
        )

        game_record = game.get_game_record_by_id(game_info_id)
        word = game_record.word

        game.update_game_record(game_info_id, False)
        game.update_account_stats(
            current_user,
            current_user.games_played + 1,
            current_user.games_win,
            current_user.games_loose + 1,
        )
        db_word = game.get_word_by_word(word)
        game.update_word_stats(
            db_word,
            db_word.times_called + 1,
            db_word.times_answered,
            db_word.times_lost + 1,
        )
        logger.info(
            f"Game ID {game_info_id} ended in loss. User: {current_user.id}, Word: {word}"
        )
        session.pop("game_info_id", None)
    return


@app.route("/exit_and_record_loss", methods=["POST"])
@login_required
def exit_and_record_loss():
    game_info_id = session.get("game_info_id")

    if game_info_id is not None:
        game = HangmanGame(
            db=db.session,
            game_settings=None,
        )
        game_record = game.get_game_record_by_id(game_info_id)
        word = game_record.word

        game.update_game_record(game_info_id, False)
        game.update_account_stats(
            current_user,
            current_user.games_played + 1,
            current_user.games_win,
            current_user.games_loose + 1,
        )
        db_word = game.get_word_by_word(word)
        game.update_word_stats(
            db_word,
            db_word.times_called + 1,
            db_word.times_answered,
            db_word.times_lost + 1,
        )
    logger.info(
        f"Game ID {game_info_id} ended in loss. User: {current_user.id}, Word: {word}"
    )
    session.pop("game_info_id", None)
    session.pop("hashed_word", None)
    session.pop("used_letters", None)
    session.pop("wrong_attempts", None)
    return redirect(url_for("index"))


@app.route("/admin/history", methods=["GET"])
@login_required
@admin_required
def admin_history():
    game = HangmanGame(
        db=db.session,
        game_settings=None,
    )
    games = game.get_all_game_records()

    return render_template("admin_history.html", games=games)


@app.route("/admin/accounts", methods=["GET", "POST"])
@login_required
@admin_required
def admin_accounts():
    game = HangmanGame(
        db=db.session,
        game_settings=None,
    )
    accounts = game.get_all_account_statistic()

    if request.method == "POST":
        account_id_to_delete = request.form.get("delete_account_id")
        if account_id_to_delete:
            account = game.get_account_by_id(account_id_to_delete)
            if account:
                game.delete_account(account)
                logger.info(
                    f"Successful deleted account for user with email: {account.email}"
                )
                flash("Account deleted successfully", "success")
            else:
                flash("Account not found", "error")

    return render_template("admin_accounts.html", accounts=accounts)


@app.route("/admin/words", methods=["GET", "POST"])
@login_required
@admin_required
def admin_words():
    game = HangmanGame(
        db=db.session,
        game_settings=None,
    )
    words = game.get_all_words()

    return render_template(
        "admin_words.html",
        words=words,
    )


@app.route("/admin/add_word", methods=["GET", "POST"])
@login_required
@admin_required
def admin_add_word():
    add_word_form = AddWordForm()

    if add_word_form.validate_on_submit():
        word = add_word_form.word.data
        word = word.upper()
        category = add_word_form.category.data
        game = HangmanGame(db=db.session, game_settings=None)

        if not game.get_word_by_word(word):
            game.create_word(word, len(word), category)
            logger.info(f"New word added: {word}, Category: {category}")
            flash("Word added successfully", "success")
        else:
            flash("This word already exists in the database", "error")

    return render_template("admin_add_word.html", add_word_form=add_word_form)


@app.route("/admin/delete_word", methods=["GET", "POST"])
@login_required
@admin_required
def admin_delete_word():
    delete_word_form = DeleteWordForm()

    if delete_word_form.validate_on_submit():
        word = delete_word_form.word.data
        game = HangmanGame(db=db.session, game_settings=None)
        db_word = game.get_word_by_word(word)

        if db_word:
            game.delete_word(db_word)
            flash("Word deleted successfully", "success")
            logger.info(f"Word deleted: {word}, Category: {db_word.category}")
        else:
            flash("This word does not exist in the database", "error")

    return render_template("admin_delete_word.html", delete_word_form=delete_word_form)


@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404


@app.errorhandler(403)
def error_403(error):
    return render_template("403.html"), 403


@app.errorhandler(500)
def error_500(error):
    return render_template("500.html"), 500
