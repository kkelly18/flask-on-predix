import os

from cf_utils import get_postgres_bindings

from . import api
from .. import db


@api.route('/')
def get_hello():
    page = ""

    if os.getenv("FLASK_CONFIG") == 'predix':
        uri, name, label = get_postgres_bindings()
        page += "<h3>{}</h3>".format(label)
        page += "<p>name: <b>{}</b></p>".format(name)
        page += "<p>uri: <b>{}</b></p>".format(uri)

    binding_uri = db.get_app()
    page += "<p>SQLALCHEMY_DATABASE_URI: {}</p>".format(binding_uri.config['SQLALCHEMY_DATABASE_URI'])

    return page
