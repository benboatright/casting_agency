#8/29/22 #Referenced Caryn's 'models.py' file to build this script unless noted otherwise #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/dc060384-b508-4a13-839e-01b636105556
from sqlalchemy import Column,Integer,String, DateTime #8/29/22 #Referenced Amy's lesson for datatypes #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/61e32678-d4aa-42f8-9767-050fef0ce9de
from flask_sqlalchemy import SQLAlchemy

database = 'casting_agency'
uri = f'postgresql://benjaminboatright@localhost:5432/{database}' #8/29/22 #Referenced Amy's lesson on connecting to the database #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/b2093f89-9b28-4d97-a02c-a829315fd3e1

db = SQLAlchemy()

def setup_db(app,uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = uri #8/29/22 #Referenced Amy's lesson on connecting to database #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/b2093f89-9b28-4d97-a02c-a829315fd3e1
    db.app = app
    db.init_app(app)
    db.create_all()

class Actors(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

class Movies(db.Model):
    __tablename__ ='movies'
    id = Column(Integer,primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)