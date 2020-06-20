

from flask import Blueprint,render_template,flash,abort,redirect,url_for
from flask_login import login_required
from  tt.forms.user import ChangeEmailForm,ChangeWeiXinForm,ChangePassword
from flask_login import current_user
from  tt.models import User
from tt.extendtions import db
from tt.utils import redirect_back,generate_token,validate_token
from tt.settings import Operation
from tt.email import send_change_email
user_bp=Blueprint('user',__name__)


@user_bp.route('/setting/weixin',methods=['GET','POST'])
@login_required
def change_weixin():

    if current_user.is_authenticated:

        form=ChangeWeiXinForm()
        if form.validate_on_submit():
            user=User.query.filter_by(id=current_user.id).first()
            if user:
                user.weixin=form.weixin.data
                db.session.commit()
                flash('微信号更改成功')
                return redirect_back()
            else:
                abort(404)

        return render_template('user/setting/change_weixin.html',form=form)
    else:
        return  redirect(url_for('main.index'))

@user_bp.route('/setting/password',methods=['GET','POST'])
@login_required
def change_password():
    form=ChangePassword()
    if form.validate_on_submit():

        user=User.query.filter_by(id=current_user.id).first_or_404()
        if user.validate_password(form.old_password.data):
            user.setpassword(form.new_password.data)
            db.session.commit()
            flash('密码更改成功','success')
            return redirect_back()
        else:
            flash('旧密码错误','danger')
            return redirect_back()
    return  render_template('user/setting/change_password.html',form=form)

@user_bp.route('setting/email',methods=['GET','POST'])
@login_required
def change_email_request():
    form=ChangeEmailForm()
    if form.validate_on_submit():
        token=generate_token(user=current_user,operation=Operation.RESET_EMAIL,new_email=form.email.data.lower())
        send_change_email(user=current_user,token=token)
        flash('请验证你的新邮箱','info')
        return redirect_back()
    return render_template('user/setting/change_email.html',form=form)


@user_bp.route('/change-email/<token>')
@login_required
def change_email(token):
    if validate_token(user=current_user, token=token, operation=Operation.CHANGE_EMAIL):
        flash('邮箱变更成功.', 'success')
        return redirect(url_for('.index', username=current_user.username))
    else:
        flash('无效的链接', 'warning')
        return redirect(url_for('.change_email_request'))















