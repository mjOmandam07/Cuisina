from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError
import cuisina_app.models as models


def validate_user(FlaskForm, field):
	chef = models.chef(user_id=field.data)
	if chef.validateUser():
		raise ValidationError('Chef already exists, check Username or Email')
	


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), validate_user])

    username = StringField('Username', validators=[DataRequired(), validate_user])

    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=5, max=20)])

    submit = SubmitField('Sign Up')
