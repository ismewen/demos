from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
import settings

from core import create_app, db
from core.context import make_context

if __name__ == '__main__':
    app = create_app(settings=settings)
    manager = Manager(app)
    migrate = Migrate(app=app, db=db)
    manager.add_command('db', MigrateCommand)
    manager.add_command('shell', Shell(make_context=make_context))
    manager.run()

