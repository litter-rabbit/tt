
from flask import Blueprint,render_template,redirect,url_for,flash
from tt.forms.auth import RegisterForm,LoginForm,ForgetForm,ResetPasswordForm
from tt.models import User
from flask_login import login_user,current_user,login_required,logout_user
from tt.extendtions import db
from tt.email import send_confirm_email,send_reset_password_email
from tt.utils import generate_token,validate_token


from tt.settings import Operation
auth_bp=Blueprint('auth',__name__)


@auth_bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form =RegisterForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        weixin=form.weeixin.data
        name=form.name.data
        user=User(email=email,name=name,weixin=weixin)
        user.setpassword(password)
        db.session.add(user)
        db.session.commit()
        flash('请验证你的邮箱，不然部分功能无法使用','success')
        token=generate_token(user,operation='confirm')
        send_confirm_email(user,token=token)
        return redirect(url_for('.login'))
    return render_template('auth/register.html',form=form)



@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.rememberme.data):

                if user.is_admin:
                    message='欢迎你：'+user.name+'超级管理员已登录'
                else:
                    message='欢迎你：'+user.name
                flash(message, 'info')
                return redirect(url_for('main.index'))
            else:
                flash('你的账号被锁定了','danger')
        else:
            flash('账号或者密码错误','danger')

        return redirect(url_for('main.index'))

    return render_template('auth/login.html',form=form)



@auth_bp.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
def confirm(token):
    if current_user.confirmed:
        redirect(url_for('main.index'))
    if validate_token(user=current_user, token=token, operation=Operation.CONFIRM):
        flash('Account confirmed', 'success')
        return redirect(url_for('main.index'))

    else:
        flash('Invalid Token or Expired ', 'danger')
        return redirect(url_for('.resend_confirm_email'))


@auth_bp.route('/forget_password',methods=['GET','POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect('main.index')
    form=ForgetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token=generate_token(user,Operation.RESET_PASSWORD)
            send_reset_password_email(user=user,token=token)
            flash('请验证你的邮箱')

        flash('请验证你的邮箱')


    return render_template('auth/forgetpassword.html')


@auth_bp.route('/resetpasswordd/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form=ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            return redirect(url_for('main.index'))

        if validate_token(user=user, token=token, operation=Operation.RESET_PASSWORD, new_password=form.password.data):
            flash('密码更新成功', 'success')
            return redirect(url_for('.login'))
        else:
            flash('无效或者过期的链接', 'danger')
            return redirect(url_for('.forget_password'))

    return render_template('auth/resetpassword.html',form=form)


@auth_bp.route('/logout')
@login_required
def logout():

    logout_user()
    flash('退出登录成功','success')

    return redirect(url_for('main.index'))



