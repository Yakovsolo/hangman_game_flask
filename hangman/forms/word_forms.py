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
from hangman import Account, current_user, Word


class AddWordForm(FlaskForm):
    word = StringField("Word", [DataRequired()])
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
    submit = SubmitField("Add word")

    def check_word(self, word):
        db_word = Word.query.filter_by(word=word.data).first()
        if db_word:
            raise ValidationError("This word already exists in database")


class DeleteWordForm(FlaskForm):
    word = StringField("Word", validators=[DataRequired()])
    submit = SubmitField("Delete word")

    def validate_word(self, field):
        db_word = Word.query.filter_by(word=field.data).first()
        if not db_word:
            raise ValidationError("This word does not exist in the database.")
