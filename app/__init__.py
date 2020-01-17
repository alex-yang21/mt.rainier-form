from flask import Flask, render_template, Response, current_app
from flask_basicauth import BasicAuth
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from flask_bootstrap import Bootstrap
from logging.handlers import RotatingFileHandler
import logging
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'
bootstrap = Bootstrap()
basic_auth = BasicAuth()
admin = Admin(name = 'Mt. Ranier Neurology', template_mode='bootstrap3')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)
    basic_auth.init_app(app)
    admin.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/mtrn.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Mt Rainier startup')

    from app.models import User, Form, FollowUp

    class AnalyticsView(BaseView):
        @expose('/')
        def index(self):
          forms_unordered = Form.query.all()
          forms_ordered = forms_unordered[::-1]
          return self.render('admin/adminaccess.html', forms=forms_ordered, admin=admin)

    class AnalyticsView1(BaseView):
        @expose('/')
        def index(self):
          forms_unordered = FollowUp.query.all()
          forms_ordered = forms_unordered[::-1]
          return self.render('admin/adminaccess1.html', forms=forms_ordered, admin=admin)

    admin.add_view(AnalyticsView(name='Patient Registration', endpoint='patient-registration'))
    admin.add_view(AnalyticsView1(name='Patient Follow-Ups', endpoint='patient-follow-ups'))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(MtRNModelView(Form, db.session))
    admin.add_view(MtRNModelView(FollowUp, db.session))

    return app

class ModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True
    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            message, 401,
           {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class MtRNModelView(ModelView):
    column_searchable_list = ('patient_name', 'timestamp')
    column_default_sort = ('timestamp', True)
