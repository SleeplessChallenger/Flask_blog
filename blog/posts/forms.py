from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):

	title = StringField('Title', validators=[DataRequired()])
	# content = TextAreaField('Content', validators=[DataRequired()])
	# we substituted for MarkDown rather than simple TextAreaField 
	content = PageDownField('You can write here', validators=[DataRequired()])
	submit = SubmitField('post it!')
