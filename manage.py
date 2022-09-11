#9/11/22 #followed the manage.py from FSND #https://github.com/udacity/FSND/blob/master/projects/capstone/heroku_sample/starter/manage.py
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app
from models import db 

migrate = Migrate(app,db)

manager = Manager(app)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()