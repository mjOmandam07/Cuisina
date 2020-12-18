from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length
import cuisina_app.models as models

##### HERE WE PUT OUR FORMS USED FOR THE FEATURE YOU ARE WORKING ##


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])

    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=5, max=20)])

    submit = SubmitField('Sign Up')
