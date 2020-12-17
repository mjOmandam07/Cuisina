from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length
import cuisina_app.models as models

class LoginForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=3, max=10)])
    submit = SubmitField('Login')