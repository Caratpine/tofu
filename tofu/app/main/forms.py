from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,SubmitField,TextField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User

class PostForm(Form):
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(Form):
    body = TextAreaField('Please enter your comment:', validators=[Required()])
    submit = SubmitField('Submit')
class SearchForm(Form):
	key = TextField('',validators=[Required()])
	submit = SubmitField('Search')