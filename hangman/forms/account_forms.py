from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed
from hangman import Account, current_user


class AccountRegistrationForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    surname = StringField("Surname", [DataRequired()])
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    repeated_password = PasswordField(
        "Repeat pssword",
        [EqualTo("password", "The password must match."), DataRequired()],
    )
    submit = SubmitField("Register")

    def check_email(self, email):
        db_account = Account.query.filter_by(email=email.data).first()
        if db_account:
            raise ValidationError("This email email address is used. Choose another.")


class AccountLoginForm(FlaskForm):
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class AccountUpdateForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    surname = StringField("Surname", [DataRequired()])
    email = StringField("Email", [DataRequired()])
    avatar = FileField("Change avatar", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")


class RequestRefreshForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Get!")

    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()
        if account is None:
            raise ValidationError(
                "There is no account registered with this email. Please register."
            )


class PasswordChangeForm(FlaskForm):
    password = PasswordField("Password", [DataRequired()])
    repeated_password = PasswordField(
        "Repeat pssword",
        [EqualTo("password", "The password must match."), DataRequired()],
    )
    submit = SubmitField("Change password")