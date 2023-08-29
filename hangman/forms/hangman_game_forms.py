from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class GameStartForm(FlaskForm):
    category = SelectField(
        "Category",
        choices=[
            ("animals", "Animals"),
            ("home", "Home"),
            ("jobs", "Jobs"),
            ("food", "Food"),
            ("clothes", "Clothes"),
            ("countries", "Countries"),
            ("cities", "Cities"),
            ("space", "Space"),
            ("mountains", "Mountains"),
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
