import os, ssl, urllib.request, urllib.parse

from flask import redirect, url_for, session, request, jsonify
from flask import current_app as app
from flask_oauthlib.client import OAuth, parse_response, _encode
from flask_oauthlib.utils import to_bytes
from copy import copy
from functools import wraps

from . import api
from . import auth
from .. import db
from .. import predix

from ..models import DataPoint


def login_required(func):
    @wraps(func)
    def token_check(*args, **kwargs):
        if 'predix_token' not in session:
            return redirect(url_for('auth.login', _external=True, _scheme=app.config['PROTOCOL']))
        return func(*args, **kwargs)
    return token_check

@api.route('/')
@login_required
def get_hello():
    page = ""
    if os.getenv("FLASK_CONFIG") == 'predix':
        page += "<h3>{}</h3>".format(app.config['SQLALCHEMY_DATABASE_LABEL'])
        page += "<p>SQLALCHEMY_DATABASE_NAME: <b>{}</b></p>".format(app.config['SQLALCHEMY_DATABASE_NAME'])

    page += "<p>SQLALCHEMY_DATABASE_URI:  <b>{}</b></p>".format(app.config['SQLALCHEMY_DATABASE_URI'])

    page += "<p><a href='{}' target='_blank'>Query Data</a></p>".format(url_for('api.get_data', _external=True, _scheme=app.config['PROTOCOL']))
    page += "<p><a href='{}'>Logout</a></p>".format(url_for('auth.logout', _external=True, _scheme=app.config['PROTOCOL']))

    return page


@api.route('/windturbine/', methods=['POST'])
@login_required
def load():
    time_series = request.json
    db.session.add_all([DataPoint.from_json(data_point) for data_point in time_series])
    db.session.commit()
    return jsonify({'return': 'ok'})


@api.route('/windturbine/', methods=['GET'])
@login_required
def get_data():
    cursor = db.session.query(DataPoint)
    return jsonify([sqla2dict(row) for row in cursor])


@auth.route('/login')
def login():
    return predix.authorize(callback=url_for('auth.authorized', _external=True, _scheme=app.config['PROTOCOL']))

@auth.route('/authorized')
def authorized():
    next_url = request.args.get('next')

    # TODO: Determine Gunicorn Worker Types to allow authorized_response() with workers > 1
    data = predix.authorized_response()

    session['predix_token'] = (
        data['access_token'],
        ''
    )

    return redirect(url_for('api.get_hello', _external=True, _scheme=app.config['PROTOCOL']))


@auth.route('/logout')
def logout():
    session.pop('predix_token', None)
    return redirect(app.config['PREDIX']['base_url'] + '/logout?redirect=' + url_for('api.get_hello', _external=True, _scheme=app.config['PROTOCOL']))

@predix.tokengetter
def get_predix_oauth_token():
    return session.get('predix_token')

def sqla2dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


