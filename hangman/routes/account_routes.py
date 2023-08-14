import os
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime
import secrets

# from PIL import Image
from flask_mail import Message, Mail
from hangman import db, app, bcrypt, mail
from hangman.forms import account_forms
from hangman.models.account import Account


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = account_forms.AccountRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        account = Account(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(account)
        db.session.commit()
        flash("You have successfully registered! You can login", "success")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = account_forms.AccountLoginForm()
    if form.validate_on_submit():
        account = Account.query.filter_by(email=form.email.data).first()
        if account and bcrypt.check_password_hash(account.password, form.password.data):
            login_user(account, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Login failed. Check email email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")


def send_reset_email(account):
    token = account.get_reset_token()
    msg = Message(
        "Slaptažodžio atnaujinimo užklausa",
        sender="pythonkursascodeacademy@gmail.com",
        recipients=[account.email],
    )
    msg.body = f"""Norėdami atnaujinti slaptažodį, paspauskite nuorodą:
    {url_for('reset_token', token=token, _external=True)}
    Jei jūs nedarėte šios užklausos, nieko nedarykite ir slaptažodis nebus pakeistas.
    """
    print(msg.body)
    # mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = account_forms.RequestRefreshForm()
    if form.validate_on_submit():
        account = Account.query.filter_by(email=form.email.data).first()
        send_reset_email(account)
        flash(
            "Jums išsiųstas el. laiškas su slaptažodžio atnaujinimo instrukcijomis.",
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
        flash("Užklausa netinkama arba pasibaigusio galiojimo", "warning")
        return redirect(url_for("reset_request"))
    form = account_forms.PasswordChangeForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        account.password = hashed_password
        db.session.commit()
        flash("Your password has been successfully changed! You can login", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
