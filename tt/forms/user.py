from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,Email



class ChangeWeiXinForm(FlaskForm):
    weixin=StringField('新微信号',validators=[DataRequired()])
    submit=SubmitField('提交')

class ChangeEmailForm(FlaskForm):
    email=StringField('新邮箱',validators=[DataRequired(),Email()])
    submit=SubmitField('提交')

class ChangePassword(FlaskForm):
    old_password=PasswordField('原密码')
    new_password=PasswordField('新密码',validators=[Length(8,16)])
    new_password2=PasswordField('再次输入密码',validators=[Length(8,16)])
    submit=SubmitField('提交')