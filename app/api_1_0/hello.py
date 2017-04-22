from flask import jsonify
from . import api


@api.route('/')
def get_hello():
    return jsonify({'hello': 'world'})
