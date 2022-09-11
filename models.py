#8/29/22 #Referenced Caryn's 'models.py' file to build this script unless noted otherwise #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/dc060384-b508-4a13-839e-01b636105556
from sqlalchemy import Column,Integer,String, DateTime #8/29/22 #Referenced Amy's lesson for datatypes #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/61e32678-d4aa-42f8-9767-050fef0ce9de
from flask_sqlalchemy import SQLAlchemy

#9/5/22 #referenced the code in the blog to hide secrets #https://dev.to/jakewitcher/using-env-files-for-environment%20#%20-variables-in-python-applications-55a1
from dotenv import load_dotenv
import os
load_dotenv('.env')

#database = os.getenv('datbase')
#user_name = os.getenv('user_name')
database_url = os.environ['DATABASE_URL']

uri = f'{database_url}' #8/29/22 #Referenced Amy's lesson on connecting to the database #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/b2093f89-9b28-4d97-a02c-a829315fd3e1

db = SQLAlchemy()

def setup_db(app,uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = uri #8/29/22 #Referenced Amy's lesson on connecting to database #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/b2093f89-9b28-4d97-a02c-a829315fd3e1
    db.app = app
    db.init_app(app)
    db.create_all() #9/11/22 #removed this based on the video here #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/e01a0ac9-68dd-4844-b399-b8fa3be667e0/concepts/336feaba-059e-4cd5-800b-3710cac58ce1

class Actors(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self,name,age,gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Movies(db.Model):
    __tablename__ ='movies'
    id = Column(Integer,primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)

    def __init__(self,title,release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()