from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from houpu import app
from exts import db

from models import User,Question,Answer

manager=Manager(app)
#migrate绑定app和db
migrate = Migrate(app,db)

manager.add_command('db', MigrateCommand)


if __name__== '__main__':
    manager.run()
