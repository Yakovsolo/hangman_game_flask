from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    BooleanField,
    StringField,
    PasswordField,
    FloatField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    ValidationError,
    EqualTo,
    Email,
    InputRequired,
)
from flask_wtf.file import FileField, FileAllowed
from hangman import Account, current_user


class GameStartForm(FlaskForm):
    category = SelectField(
        "Category",
        choices=[
            "animals",
            "home",
            "jobs",
            "food",
            "clothes",
            "countries",
            "cities",
            "space",
            "mountains",
        ],
        validators=[InputRequired(message="Please select a category.")],
    )
    difficulty = SelectField(
        "Difficulty",
        choices=[
            "Easy",
            "Medium",
            "Hard",
        ],
    )

    start_game = SubmitField("Start game!")


class GamePlayForm(FlaskForm):
    letter = StringField("Letter", [DataRequired()])
    submit_enter = SubmitField("Enter")
    submit_restart = SubmitField("Restart game!")
    submit_start_new_game = SubmitField("Start new game!")
    submit_exit = SubmitField("Exit")
