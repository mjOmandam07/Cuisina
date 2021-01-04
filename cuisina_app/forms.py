from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError
import cuisina_app.models as models




class CreatePost(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	upload_picture = FileField('Upload Picture',  validators=[FileAllowed(['jpg', 'png'])])
	cuisine = SelectField('Cusine', choices=[('','Select Cuisine'),('Filipino','Filipino'),('Western','Western'),('Asian','Asian'),('European','European')], validators=[DataRequired()])
	submit = SubmitField('Post')

class rateForm(FlaskForm):
    rate = RadioField('rate', choices=[('5',''),('4',''),('3',''),('2',''),('1','')],validators=[DataRequired()])
    submit = SubmitField('Rate it')

class addCommment(FlaskForm):
	comment = TextAreaField('Content', validators=[DataRequired()])
	submit = SubmitField('Add Comment')