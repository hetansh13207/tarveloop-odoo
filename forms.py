from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    DateField
)
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=2, max=100)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")

class TripForm(FlaskForm):

    title = StringField(
        "Trip Title",
        validators=[DataRequired()]
    )

    description = StringField(
        "Description"
    )

    start_date = DateField(
        "Start Date",
        format="%Y-%m-%d"
    )

    end_date = DateField(
        "End Date",
        format="%Y-%m-%d"
    )

    budget = StringField(
        "Budget"
    )

    submit = SubmitField("Create Trip")

class StopForm(FlaskForm):

    city = StringField(
        "City",
        validators=[DataRequired()]
    )

    country = StringField(
        "Country",
        validators=[DataRequired()]
    )

    start_date = DateField(
        "Start Date",
        format="%Y-%m-%d"
    )

    end_date = DateField(
        "End Date",
        format="%Y-%m-%d"
    )

    submit = SubmitField("Add Stop")


class ActivityForm(FlaskForm):

    title = StringField(
        "Activity",
        validators=[DataRequired()]
    )

    category = StringField(
        "Category"
    )

    cost = StringField(
        "Cost"
    )

    notes = StringField(
        "Notes"
    )

    submit = SubmitField("Add Activity")

class PackingForm(FlaskForm):

    item_name = StringField(
        "Item",
        validators=[DataRequired()]
    )

    submit = SubmitField("Add Item")

class NoteForm(FlaskForm):

    content = StringField(
        "Note",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Note")

class ProfileForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[DataRequired()]
    )

    profile_image = FileField(
        "Profile Image"
    )

    submit = SubmitField("Update Profile")


