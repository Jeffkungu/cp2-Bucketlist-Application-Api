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

# define a new command to automate testing
# def run_tests():
#     """Allows us to run the unit tests without test coverage."""
#     tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.wasSuccessful():
#         return 0
#     return 1
def create_db(dbname):
    os.system("createdb " + dbname)

def drop_db(dbname):
    os.system("dropdb " + dbname)
    
if __name__ == '__main__':
    manager.run()