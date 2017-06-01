import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from bucketlistapp import db, create_app
from bucketlistapp import models

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

# set up a command for migrating db
manager.add_command('db', MigrateCommand)


def create_db(dbname):
    os.system("createdb " + dbname)


def drop_db(dbname):
    os.system("dropdb " + dbname)


if __name__ == '__main__':
    manager.run()
