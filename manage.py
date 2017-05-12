#!/usr/bin/env python
import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app import create_app, logger, db


flask_config = os.getenv('FLASK_CONFIG') or 'development'
if flask_config == 'development':
    logger.info("Using development config")

logger.info("configured as: {}".format(flask_config))

app = create_app(flask_config)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('runserver', Server(host='127.0.0.1', port=4999))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
