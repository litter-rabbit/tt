


from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_whooshee import Whooshee
from flask_wtf import CSRFProtect
from flask_migrate import Migrate




db=SQLAlchemy()
bootstrap=Bootstrap()
login_manager=LoginManager()
mail=Mail()
moment=Moment()
whooshee=Whooshee()
csrf = CSRFProtect()
migrate=Migrate()



@login_manager.user_loader
def load_user(user_id):
    from tt.models import User
    return User.query.get(int(user_id))


login_manager.login_view = 'auth.login'

