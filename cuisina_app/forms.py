from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, PasswordField, TextAreaField, RadioField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email
from wtforms.fields.html5 import DateField
import cuisina_app.models as models

	
class LoginForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
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
    age = DateField('Birthday', format='%Y-%m-%d')
    register_gender = SelectField('Gender:', choices=[('','Choose...'),('Male','Male'),('Female','Female')], validators=[DataRequired()])
    upload_picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save Profile')




class CreatePost(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    upload_picture = FileField('Upload Picture',  validators=[FileAllowed(['jpg', 'png'])])
    cuisine = SelectField('Cusine', choices=[('','Select Cuisine'),('Filipino','Filipino'),('Western','Western'),('Chinese','Chinese'),('European','European'),('Italian','Italian'),('Indian','Indian'),('French','French'),('Japanese','Japanese'),('Mexican','Mexican'),('Thai','Thai'),('Turkish','Turkish'),('Korean','Korean'),('Spanish','Spanish'),('Middle Eastern','Middle Eastern')], validators=[DataRequired()])
    submit = SubmitField('Post')

class rateForm(FlaskForm):
    rate = RadioField('rate', choices=[('5',''),('4',''),('3',''),('2',''),('1','')],validators=[DataRequired()])
    submit = SubmitField('Rate it')

class addCommment(FlaskForm):
    comment = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Comment')