from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, Email
import cuisina_app.models as models

	
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')





class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=5, max=20)])

    submit = SubmitField('Sign Up')

