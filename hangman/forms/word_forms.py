from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class AddWordForm(FlaskForm):
    word = StringField("Word", [DataRequired()])
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
    submit = SubmitField("Add word")


class DeleteWordForm(FlaskForm):
    word = StringField("Word", validators=[DataRequired()])
    submit = SubmitField("Delete word")
