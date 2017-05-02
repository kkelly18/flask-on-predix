import os

from flask import jsonify, request

from . import api
from .. import db
from ..models import DataPoint

from cf_utils import get_postgres_bindings


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


@api.route('/windturbine/', methods=['POST'])
def load():
    time_series = request.json
    db.session.add_all([DataPoint.from_json(data_point) for data_point in time_series])
    db.session.commit()
    return jsonify({'return': 'ok'})


@api.route('/windturbine/', methods=['GET'])
def get_data():
    cursor = db.session.query(DataPoint)
    return jsonify([sqla2dict(row) for row in cursor])


def sqla2dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}
