from flask import Blueprint

api = Blueprint('api', __name__)
auth = Blueprint('auth', __name__)

from . import hello
