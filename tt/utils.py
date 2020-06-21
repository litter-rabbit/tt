

from flask import current_app,request,redirect,url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature,SignatureExpired
from tt.settings import Operation
from tt.models import User
from tt.extendtions import db

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)

    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)



def validate_token(user,token,operation,new_password=None):
    s=Serializer(current_app.config['SECRET_KEY'])

    try:
        data=s.loads(token)
    except (BadSignature,SignatureExpired):
        return False

    if data.get('operation') != operation or data.get('id') != user.id:
        return False

    if operation == Operation.CONFIRM:
        user.confirmed=True
    elif operation == Operation.RESET_PASSWORD:
        user.setpassword(new_password)
    elif operation == Operation.RESET_EMAIL:
        new_email=data.get('new_email')
        if new_email == None:
            return False
        elif User.query.filter_by(email=new_email).first() != None:
            return False
        user.email=new_email
    else:
        return False

    db.session.commit()
    return True

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

