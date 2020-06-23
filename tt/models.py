

from tt.extendtions import db,whooshee
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@whooshee.register_model('area','name')
class Player(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(128))
    rank=db.Column(db.Integer)
    backup=db.Column(db.String(256))
    area=db.Column(db.String(32))
    is_buy=db.Column(db.Boolean,default=False)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    user=db.relationship('User',back_populates='players')


@whooshee.register_model('name','weixin')
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(64),unique=True)
    name=db.Column(db.String(64),unique=True)
    weixin = db.Column(db.String(64))
    password_hash=db.Column(db.String(64))
    points=db.Column(db.Integer,default=20)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)
    confirmed=db.Column(db.Boolean,default=False)
    active=db.Column(db.Boolean,default=True)
    is_admin=db.Column(db.Boolean,default=False)
    players=db.relationship('Player',back_populates='user',cascade='all')

    @property
    def is_active(self):
        return self.active

    def setpassword(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)



class Website(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    infomation=db.Column(db.Text)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)


class Advice(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(256))
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)
    username=db.Column(db.String(64))
    email=db.Column(db.String(64))
    is_read=db.Column(db.Boolean,default=False)










