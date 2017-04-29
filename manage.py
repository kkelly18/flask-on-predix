#!/usr/bin/env python

import os
from flask_script import Manager, Server

from app import create_app, logger

flask_config = os.getenv('FLASK_CONFIG')
logger.info("configured as: {}".format(flask_config))

if not flask_config:
    logger.info("Using development config")
    flask_config = 'development'

app = create_app(flask_config)
manager = Manager(app)

manager.add_command('runserver', Server(host='127.0.0.1', port=4999))

if __name__ == '__main__':
    manager.run()
