

from flask import Flask,render_template
from tt.settings import config
from tt.extendtions import db,login_manager,bootstrap,mail,moment,whooshee,csrf
from tt.blueprints.main import main_bp
from tt.blueprints.auth import auth_bp
from tt.blueprints.user import user_bp
from tt.blueprints.admin import admin_bp
from tt.blueprints.ajax import ajax_bp
import click
from tt.models import User,Website


import os

def create_app(configname=None):
    if not configname:
        configname=os.getenv('FLASK_CONFIG','development')

    app=Flask('tt')

    app.config.from_object(config[configname])
    register_extendtions(app)
    register_blueprints(app)
    register_command(app)
    register_errorhandlers(app)

    return app


def  register_extendtions(app):
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    whooshee.init_app(app)
    csrf.init_app(app)





def register_blueprints(app):

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(user_bp,url_prefix='/user')
    app.register_blueprint(admin_bp,url_prefix='/nimda')
    app.register_blueprint(ajax_bp,url_prefix='/ajax')


def register_command(app):

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def initadmin():
        """Initialize the admin."""
        admin=User(email='709343607@qq.com',is_admin=True,name='lrabbit',weixin='bigboss')
        admin.setpassword('12345678')
        db.session.add(admin)
        db.session.commit()
        click.echo('Initialized admin.')

    @app.cli.command()
    def initwebsite():
        """Initialize the admin."""
        website = Website(infomation='欢迎来到本站')

        db.session.add(website)
        db.session.commit()
        click.echo('Initialized website.')










def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

