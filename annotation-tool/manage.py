#!/usr/bin/env python
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import os
from app import create_app, db
from app.models import User, Role, Picture, Label
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand, upgrade

#print "******LOADING  ENVIROMENT MANUALLY" 
#os.environ['FLASK_CONFIG'] = 'production'
#print "Production enviroment loaded"

enviroment_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

if os.path.exists(enviroment_file):
    print('Importing environment from .env...')
    for line in open(enviroment_file):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User,
                Role=Role, Label=Label, Picture=Picture)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


## otra forma de definir los comandos para el manager
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def import_pictures():
    """Import the pictures from the import folder and add them to the database"""
    from tools import importer
    origin = app.config['IMPORT_FOLDER']
    destiny = app.config['IMPORTED_PICTURES_FOLDER']
    context = dict(app=app, db=db, User=User, Label=Label, Picture=Picture, route=origin, destiny=destiny)
    importer.load(context)

@manager.command
def import_pictures_simplified():
    """Import the pictures from the import folder and add them to the database"""
    from tools import importer_simplified
    origin = app.config['IMPORT_FOLDER']
    destiny = app.config['IMPORTED_PICTURES_FOLDER']
    context = dict(app=app, db=db, User=User, Label=Label, Picture=Picture, route=origin, destiny=destiny)
    importer_simplified.load(context)


@manager.command
def deploy():
    """Create the database, tables and needed users, roles, and labels"""
    from tools import deploy
    #upgrade() shouldn't be necessary
    context = dict(app=app, db=db, User=User, Label=Label, Role=Role)
    deploy.initial_deploy(context)







if __name__ == '__main__':
    manager.run()
