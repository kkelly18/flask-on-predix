import logging
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class PredixConfig(Config):
    pass


config = {'development': DevelopmentConfig,
 'testing': TestingConfig,
 'predix': PredixConfig,
 'default': DevelopmentConfig}
