#!/usr/bin/env python
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import os
from app import create_app, db
from app.models import User, Role, Picture, Label
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

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
def importsuite():
    from importtools import importer

    IMPORT_FOLDER_NAME = "import bucket"
    route = os.path.join(os.path.dirname(os.path.abspath(IMPORT_FOLDER_NAME)), IMPORT_FOLDER_NAME)
    context = dict(app=app, db=db, User=User, Label=Label, Picture=Picture)
    importer.load(route, context)







if __name__ == '__main__':
    manager.run()
