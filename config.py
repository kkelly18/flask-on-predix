import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    TESTING = False

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True


class PredixConfig(Config):

    @staticmethod
    def getDatabaseUri():

        # Extract VCAP_SERVICES
        vcap_services = os.getenv("VCAP_SERVICES")
        if vcap_services is not None:
            decoded_config = json.loads(vcap_services)
            jdbc_uri = None
            postgres = decoded_config['postgres'][0]['credentials']
            if postgres is not None:
                jdbc_uri = postgres['jdbc_uri']
                database_name = postgres['database']
                username = postgres['username']
                password_str = postgres['password']
                db_host = postgres['host']
                db_port = postgres['port']
                print("jdbs uri= %s , dbname=%s, username=%s, pwd=%s, host = %s, port=%s" % (jdbc_uri, database_name, username, password_str, db_host, db_port))
                return "postgres://{}:{}@{}:{}/{}".format(username, password_str, db_host, db_port, database_name)
        return None

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


    SQLALCHEMY_DATABASE_URI = getDatabaseUri.__func__()#os.environ.get('PROD_DATABASE_URL')

config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'predix': PredixConfig,
          'default': DevelopmentConfig}
