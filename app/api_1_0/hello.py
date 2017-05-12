import os, ssl, urllib.request, urllib.parse

from flask import redirect, url_for, session, request, jsonify
from flask import current_app as app
from flask_oauthlib.client import OAuth, OAuthException, parse_response, _encode
from flask_oauthlib.utils import to_bytes
from oauthlib.common import to_unicode
from copy import copy

from . import api
from . import auth
from .. import db
from .. import predix

from ..models import DataPoint

from cf_utils import get_postgres_bindings


@api.route('/')
def get_hello():
    if 'predix_token' in session:
        page = ""
        if os.getenv("FLASK_CONFIG") == 'predix':
            uri, name, label = get_postgres_bindings()
            page += "<h3>{}</h3>".format(label)
            page += "<p>name: <b>{}</b></p>".format(name)
            page += "<p>uri: <b>{}</b></p>".format(uri)

        page += "<p>SQLALCHEMY_DATABASE_URI: {}</p>".format(app.config['SQLALCHEMY_DATABASE_URI'])

        page += "<br /><p><a href='{}'>Logout</a></p>".format(url_for('auth.logout', _external=True, _scheme=app.config['PROTOCOL']))

        return page
    return redirect(url_for('auth.login', _external=True, _scheme=app.config['PROTOCOL']))


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


@predix.tokengetter
def get_predix_oauth_token():
    return session.get('predix_token')


@auth.route('/login')
def login():
    return predix.authorize(callback=url_for('auth.authorized', _external=True, _scheme=app.config['PROTOCOL']))

@auth.route('/authorized')
def authorized():
    next_url = request.args.get('next')

    # OAuth.remote_app.authorized_response() doesn't work when pushed to Predix (tries to use auth_code twice)
    # Manual authorized_response based on https://github.com/lepture/flask-oauthlib/blob/master/flask_oauthlib/client.py
    client = predix.make_client()
    remote_args = {
        'code': request.args.get('code'),
        'client_secret': predix.consumer_secret,
        'redirect_uri': url_for('auth.authorized', _external=True, _scheme=app.config['PROTOCOL'])
    }
    
    remote_args.update(predix.access_token_params)
    headers = copy(predix._access_token_headers)
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    body = client.prepare_request_body(**remote_args)

    response, content = predix.http_request(
        predix.expand_url(predix.access_token_url),
        headers=headers,
        data=to_bytes(body, predix.encoding),
        method=predix.access_token_method,
    )

    data = parse_response(response, content, content_type=predix.content_type)

    session['predix_token'] = (
        data['access_token'],
        ''
    )

    return redirect(url_for('api.get_hello', _external=True, _scheme=app.config['PROTOCOL']))


@auth.route('/logout')
def logout():
    session.pop('predix_token', None)
    session.clear()
    return redirect(app.config['PREDIX']['base_url'] + '/logout?redirect=' + url_for('api.get_hello', _external=True, _scheme=app.config['PROTOCOL']))

def sqla2dict(model):
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}
