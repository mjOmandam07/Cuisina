from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email
import cuisina_app.models as models


##### HERE WE PUT OUR FORMS USED FOR THE FEATURE YOU ARE WORKING ##
class ProfileForm(FlaskForm):
    fname = StringField('First Name:',
                        validators=[DataRequired(), Length(min=2, max=32)])
    lname = StringField('Last Name:',
                        validators=[DataRequired(), Length(min=2, max=32)])
    email = StringField('Email Address:',
                        validators=[DataRequired(), Email()])
    age = StringField('Age:',
                      validators=[DataRequired(), Length(min=1, max=3)])
    register_gender = SelectField('Gender:', choices=['Choose...', ('Male', 'Male'), ('Female', 'Female')],
                                  validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')
