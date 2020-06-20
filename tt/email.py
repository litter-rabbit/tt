

from tt.extendtions import mail
from  flask import current_app,render_template
from flask_mail import Message
from threading import Thread

def _send_async_mail(app,message):
    with app.app_context():
        mail.send(message)

def send_mail(to,subject,template,**kwargs):
    message=Message(current_app.config['TT_MAIL_SUBJECT_PREFIX']+subject,recipients=[to])
    message.body=render_template(template+'.txt',**kwargs)
    message.html=render_template(template+'.html',**kwargs)
    app=current_app._get_current_object()
    thr = Thread(target=_send_async_mail,args=[app,message])
    thr.start()
    return thr


def send_confirm_email(user,token,to=None):
    send_mail(subject='Email Confirm',to=to or user.email,token=token,user=user,template='emails/confirm')

def send_change_email(user,token,to=None):
    send_mail(subject='Email Change',to=to or user.email,token=token,user=user,template='emails/change_email')

def send_reset_password_email(user,token,to=None):
    send_mail(subject='Email Reset Password',to=to or user.email,token=token,user=user,template='emails/reset_password')




