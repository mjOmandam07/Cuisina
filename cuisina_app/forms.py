from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
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


class ProfileForm(FlaskForm):
    username = StringField('Username:',
                        validators=[DataRequired(), Length(min=2, max=32)])
    fname = StringField('First Name:',
                        validators=[DataRequired(), Length(min=2, max=32)])
    lname = StringField('Last Name:',
                        validators=[DataRequired(), Length(min=2, max=32)])
    email = StringField('Email Address:', validators=[DataRequired(), Email()])
    age = StringField('Age:',
                      validators=[DataRequired(), Length(min=1, max=3)])
    register_gender = SelectField('Gender:', choices=[('','Choose...'),('Male','Male'),('Female','Female')], validators=[DataRequired()])
    upload_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save Profile')

