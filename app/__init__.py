import logging
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger("flask_on_predix")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(process)-7s %(name)-20s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


from config import config
from cf_utils import get_postgres_bindings


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    tc = config[config_name]
    if config_name == 'predix':
        bindings = get_postgres_bindings()
        tc.SQLALCHEMY_DATABASE_URI = bindings[0]

    app.config.from_object(tc)

    db.init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
