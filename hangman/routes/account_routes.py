import logging
import logging.config
import os
import secrets
from functools import wraps
from os import path

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from PIL import Image

from hangman import app, bcrypt, db, mail
from hangman.forms import account_forms
from hangman.forms.account_forms import AccountUpdateForm
from hangman.game import HangmanGame
from hangman.models.account import Account

log_file_path = path.join(path.dirname(path.abspath(__file__)), "../logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Administrator rights are required to access this page.", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    from hangman import AccountCrud

    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = account_forms.AccountRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_account = AccountCrud(db=db.session)
        if new_account.create_account(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=hashed_password,
        ):
            flash("You have successfully registered! You can login", "success")
            return redirect(url_for("index"))
        else:
            flash("Email already exists. Please choose a different email.", "danger")
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = account_forms.AccountLoginForm()
    if form.validate_on_submit():
        print("AAAAAAAAAAAAAAAAAAAAA")
        account = Account.query.filter_by(email=form.email.data).first()
        print(account)
        if account and bcrypt.check_password_hash(account.password, form.password.data):
            login_user(account, remember=form.remember.data)
            logger.info(f"Successful login for user with email: {account.email}")

            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            logger.warning(
                f"Failed login attempt for user with email: {form.email.data}"
            )
            flash("Login failed. Check email email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/admin")
@login_required
@admin_required
def admin():
    return render_template("admin.html")


def send_reset_email(account):
    token = account.get_reset_token()
    msg = Message(
        "Password update request",
        sender="hangman_game@rambler.ru",
        recipients=[account.email],
    )
    msg.body = f"""To update your password, click on the link:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request, do nothing and the password will not be changed.
    """
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = account_forms.RequestRefreshForm()
    if form.validate_on_submit():
        account = Account.query.filter_by(email=form.email.data).first()
        send_reset_email(account)
        flash(
            "Email sent to you email with password reset instructions.",
            "info",
        )
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    account = Account.verify_reset_token(token)
    if account is None:
        flash("The request is invalid or expired", "warning")
        return redirect(url_for("reset_request"))
    form = account_forms.PasswordChangeForm()
    if form.validate_on_submit():
        account.reset_password(form.password.data)
        flash("Your password has been successfully changed! You can login", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/avatars", picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account_view():
    return render_template("account_view.html", account_data=current_user)


@app.route("/account/update", methods=["GET", "POST"])
@login_required
def account_update():
    form = AccountUpdateForm()
    game = HangmanGame(
        db=db.session,
        game_settings=None,
    )
    if form.validate_on_submit():
        if form.avatar.data:
            avatar = save_picture(form.avatar.data)
            current_user.avatar = avatar
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        avatar = current_user.avatar
        game.update_account_data(current_user, name, surname, email, avatar)
        flash("Your account updated!", "success")
        return redirect(url_for("account_view"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.email.data = current_user.email

    avatar = url_for("static", filename="\\avatars\\" + current_user.avatar)
    return render_template(
        "account_update.html", title="Account", form=form, avatar=current_user.avatar
    )
