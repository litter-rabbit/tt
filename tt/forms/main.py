
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField
from wtforms.validators import Optional,DataRequired,Email

class PlayerForm(FlaskForm):
    name=StringField('球员名称',validators=[DataRequired()])
    rank=SelectField('球员等级',coerce = int,choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10')])
    backup=StringField('备注',validators=[Optional()])
    submit=SubmitField('提交')



class AdviceForm(FlaskForm):
    body=TextAreaField('建议内容',validators=[DataRequired()])
    email=StringField('联系邮箱',validators=[Optional(),Email()])
    submit=SubmitField('提交')
