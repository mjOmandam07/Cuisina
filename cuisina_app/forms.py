from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError



class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=5, max=20)])

    submit = SubmitField('Sign Up')
