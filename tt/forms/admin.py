from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField


class WebsiteForm(FlaskForm):
    information=TextAreaField('公告')
    submit=SubmitField('提交')
