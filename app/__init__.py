import logging, sys, urllib.request

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth


logger = logging.getLogger("flask_on_predix")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(process)-7s %(name)-20s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

from cf_utils import get_postgres_bindings


db = SQLAlchemy()
oauth = OAuth()
predix = oauth.remote_app(
    'predix',
    app_key='PREDIX'
)

from .models import DataPoint


def create_app(config_name):
    app = Flask(__name__)

    if (config_name == 'development'):
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.PredixConfig')
        app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_DATABASE_NAME'], app.config['SQLALCHEMY_DATABASE_LABEL'] = get_postgres_bindings()

    app.config['PREDIX'] = dict(
        request_token_url = None,
        access_token_method = 'POST',
        base_url = app.config['UAA_URL'],
        access_token_url = app.config['UAA_URL'] + '/oauth/token',
        authorize_url = app.config['UAA_URL'] + '/oauth/authorize',
        consumer_key = app.config['CLIENT_ID'],
        consumer_secret = app.config['CLIENT_SECRET']
    )

    db.init_app(app)
    oauth.init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    from .api_1_0 import auth as auth_1_0_blueprint

    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    app.register_blueprint(auth_1_0_blueprint, url_prefix='/auth')

    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(debuglevel=app.config['URLLIB_REQUEST_DEBUG_LEVEL'], context=app.config['CONTEXT']))
    urllib.request.install_opener(opener)

    return app