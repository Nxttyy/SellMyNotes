from flask_wtf import FlaskForm
from wtforms import StringField
from flask_wtf.file import FileField, FileRequired

class FileUploadForm(FlaskForm):
	title = StringField('Title')
	note = FileField('File', validators=[FileRequired()])