from werkzeug import security
from flask import json
import os, base64, ssl

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = security.gen_salt(32)
    DEBUG = False
    TESTING = False
    URLLIB_REQUEST_DEBUG_LEVEL = 0

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


class DevelopmentConfig(Config):
    DEBUG = True
    URLLIB_REQUEST_DEBUG_LEVEL = 1

    PROTOCOL = 'http'
    CONTEXT = ssl._create_unverified_context()

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    UAA_URL = '<UAA_TARGET>'
    CLIENT_ID = '<UAA_CLIENT_ID>'
    CLIENT_SECRET = '<UAA_CLIENT_SECRET>'


class PredixConfig(Config):
    PROTOCOL = 'https'
    CONTEXT = ssl._create_default_https_context()

    if os.getenv('VCAP_SERVICES'):
        UAA_URL = json.loads(os.getenv('VCAP_SERVICES'))['predix-uaa'][0]['credentials']['uri']
        CLIENT_ID, CLIENT_SECRET = base64.b64decode(bytes(os.getenv('base64ClientCredential'), 'utf-8')).decode().split(':')