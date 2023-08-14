import os
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime
import secrets

# from PIL import Image
from flask_mail import Message, Mail
from hangman import db, app, bcrypt, mail
from hangman.forms.word_forms import *
from hangman.models.account import Account


@app.route("/admin/add_word", methods=["GET", "POST"])
@login_required
def admin_add_word():
    form = AddWordForm()
    if form.validate_on_submit():
        word = form.word.data
        category = form.category.data
        # Добавление слова в базу данных
        flash(f"The word '{word}' in category '{category}' has been added.", "success")
        return redirect(url_for("index"))

    return render_template("add_word.html", form=form)


@app.route("/admin/delete_word", methods=["GET", "POST"])
@login_required
def admin_delete_word():
    form = DeleteWordForm()
    if form.validate_on_submit():
        word = form.word.data
        # Добавление слова в базу данных
        flash(f"The word '{word}' has been deleted from database.", "success")
        return redirect(url_for("admin_delete_word"))

    return render_template("delete_word.html", form=form)
