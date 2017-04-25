from flask import jsonify, request
from . import api
from .. import db
from ..models import DataPoint, from_json
def sqla2dict(model):
    """ Declarative Base model to dict """
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}

@api.route('/')
def get_hello():
    return jsonify({'hello': 'world'})


@api.route('/load/', methods=['POST'])
def load():
    objs = request.json
    db.session.add_all([from_json(obj) for obj in objs])
    db.session.commit()
    return jsonify({'return': 'ok'})


@api.route('/data/', methods=['GET'])
def getData():
    objs = db.session.query(DataPoint)
    return jsonify([sqla2dict(i) for i in objs])

