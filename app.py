import json
import os
from platform import release
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from urllib.request import urlopen #9/5/22 #referenced this code to remember how to perform authorizations #https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
from jose import jwt #9/5/22 #referenced this code to remember how to perform authorizations #https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
from functools import wraps #9/5/22 #referenced this code to remember how to perform authorizations #https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
from models import setup_db,Actors,Movies
#9/5/22 #referenced the code in the blog to hide secrets #https://dev.to/jakewitcher/using-env-files-for-environment%20#%20-variables-in-python-applications-55a1
from dotenv import load_dotenv
load_dotenv('.env')

# how to generate new tokens
#https://dev-dy086z0n.us.auth0.com/authorize?audience=casting&response_type=token&client_id=z1jPPMPtpmyyDmrOFsNsRIH7rdHDdD9x&redirect_uri=http://localhost:8080/login-results

user_name = os.getenv('user_name')
database = os.getenv('database')
domain = os.getenv('auth_domain')
api = os.getenv('api')

uri = f'postgresql://{user_name}@{database}' #8/29/22 #Referenced Amy's lesson on connecting to the database #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/b2093f89-9b28-4d97-a02c-a829315fd3e1

# Authorization Methods
# 9/5/22 #referenced this code to perform get token #https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
# this method retreives the bearer token from a request submitted
def retreive_token():
  # retreive the Authorization
  token_request = request.headers.get('Authorization')
  # split the authorization and get the bearer phrase
  bearer = token_request.split(' ')[0]
  # split the authorization and get the token
  token = token_request.split(' ')[1]
  # if the authorization did not exist, abort 401
  if token_request is None:
    abort(401)
  # if the authorization was not a bearer token, abort 401
  elif bearer.lower() != 'bearer':
    abort(401)
  # return the token
  else:
    return token

# Verify and Decode the JWT
# 9/5/22 #referenced this code to verify and decode #https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
def ver_and_decode_jwt(token):
  # set the well-known jwks.json url
  well_known_url = urlopen(f'https://{domain}/.well-known/jwks.json')
  # read the data from the well_known_url and change it to json
  well_known_data = json.loads(well_known_url.read())
  # retreive the unverfiied header using the token
  unver_header = jwt.get_unverified_header(token)
  # init the rsa_key
  rsa_key = {}
  # run through all the keys in the data
  for key in well_known_data['keys']:
    # if the 'kid' from one of the keys matches the 'kid from the unverified header, populate the rsa_key dictionary
    if key['kid'] == unver_header['kid']:
      rsa_key = {
        'kty':key['kty'],
        'kid':key['kid'],
        'use':key['use'],
        'n':key['n'],
        'e':key['e']
      }
  # if the rsa_key was populated try to decode and return the payload
  if rsa_key is not None:
    try:
      payload = jwt.decode(token,rsa_key,algorithms=['RS256'],audience=api,issuer=f'https://{domain}/')
      return payload
    except:
      abort(401)

# Build the require_authorization method
# 9/5/22 #referenced this code to add in permissions #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/1e1c8e9d-61af-4a0a-b7d5-87e5becf9be7/concepts/b4d79d5c-3d79-43e6-93ca-0d750043a373
def check_perms(permission,payload):
  if permission not in payload['permissions']:
    abort(403)
  else:
    return True

# 9/5/22 #referenced this code to build this method #https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
def require_auth(permission=''):
  def require_authorization_decor(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
      # retreive the token
      token = retreive_token()
      try:
        # get the payload using the ver_and_decode_jwt method and the token
        payload = ver_and_decode_jwt(token)
      except:
        abort(401)
       # make sure that the payload included the permission associated with a given endpoint 
      check_perms(permission,payload) # 9/5/22 #referenced this code to add in permissions #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/1e1c8e9d-61af-4a0a-b7d5-87e5becf9be7/concepts/b4d79d5c-3d79-43e6-93ca-0d750043a373
      return f(payload,*args,**kwargs)
    return wrapper
  return require_authorization_decor
    

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app,uri)

  @app.route('/',methods=['GET']) 
  def test():
      return 'this is a test'

  # this endpoint gets all the movies form the data table
  @app.route('/movies',methods=['GET'])
  @require_auth(permission='get:movies')
  def get_movies(payload):
    # query all the movies from the table
    all_movies = Movies.query.all()
    # initialize a list to store the movies
    movies_list = []
    # for each movie in the table, create a dictionary with success, id, title, and release date.
    # then append each dictionary to the list 
    for movie in all_movies:
      movie_dict = {
        'success': True,
        'id': movie.id,
        'title': movie.title,
        'release_date': movie.release_date
      }
      movies_list.append(movie_dict)
    # return the jsonifyied list
    return jsonify(movies_list)

  # this endpoint retreives all the actors form the table
  @app.route('/actors',methods=['GET'])
  @require_auth(permission='get:actors')
  def get_actors():
    # query all the actors from the table
    all_actors = Actors.query.all()
    # init a list to hold the actors 
    actors_list = []
    # for each actor in the table, fill out a dictionary with success, id, name, age, and gender.
    # then append each of the dictionaries to the list
    for actor in all_actors:
      actor_dict = {
        'success' : True,
        'id' : actor.id,
        'name': actor.name,
        'age': actor.age,
        'gender': actor.gender
      }
      actors_list.append(actor_dict)
    # return the list
    return jsonify(actors_list)

  # this endpoint deletes a movie from the table based in the <id> passed in the route handler
  @app.route('/movies/<id>',methods=['DELETE'])
  @require_auth(permission='delete:movies')
  def delete_movie(id):
    # query the movie with the id from the route handler
    movie = Movies.query.get(id)
    # if the movie id is in the table, delete it and return the success dictionary
    if movie is not None:
      movie.delete()
      return jsonify({
        'success': True,
        'id_deleted':id
      })
    # else, return the fail dictionary
    else:
      return jsonify({
        'success': False,
        'id':'The id provided is not in the table'
      })

  # this endpoint deletes an actor from the table based on the <id> passed in teh route handler
  @app.route('/actors/<id>',methods=['DELETE'])
  @require_auth(permission='delete:actors')
  def delete_actor(id):
    # query the actor with the id form the route handler
    actor = Actors.query.get(id)
    # if the actor is in the tbale, delete it and return the success
    if actor is not None:
      actor.delete()
      return jsonify({
        'success': True,
        'id': id
      })
    # else, return the fail dictionary
    else:
      return jsonify({
        'success': False,
        'id': 'The id provided is not in the table'
      })

  # this endpoint posts a new movie to the table based on the request made
  @app.route('/movies',methods=['POST'])
  @require_auth(permission='post:movies')
  def add_movie():
    movie = request.get_json() #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
    if movie.get('title') is not None and movie.get('release_date') is not None: #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
      new_movie = Movies(title=movie.get('title'),
                         release_date=movie.get('release_date')) #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
      new_movie.insert()
      return jsonify({
        'success': True,
        'title':movie.get('title'), #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
        'release_date':movie.get('release_date') #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
      })
    else:
      return jsonify({
        'success':False,
      })
  
  # this endpoint posts a new actor to the table based on teh request
  @app.route('/actors',methods=['POST'])
  @require_auth(permission='post:actors')
  def add_actors():
    actor = request.get_json() #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
    if actor.get('name') is not None and actor.get('age') is not None and actor.get('gender') is not None: #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
      new_actor = Actors(name=actor.get('name'),
                         age=actor.get('age'),
                         gender=actor.get('gender')) #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
      new_actor.insert()
      return jsonify({
        'success': True,
        'name':actor.get('name'), #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
        'age':actor.get('age'), #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
        'gender':actor.get('gender') #8/31/22 #Referenced Caryn's code to remember how to get the request #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
      })
    else:
        return jsonify({
          'success':False
        })
  
  # this endpoint patches a new movie
  @app.route('/movies/<id>',methods=['PATCH'])
  @require_auth(permission='patch:movies')
  def edit_movie(id):
    movie_request = request.get_json()
    movie = Movies.query.get(id)

    if movie_request.get('title') is not None or movie_request.get('release_date') is not None:
      # determine the title to update
      if movie_request.get('title') is not None:
        movie.title = movie_request.get('title')
      # determine the release date to update
      if movie_request.get('release_date') is not None:
        movie.release_date = movie_request.get('release_date')
      # make the update
      movie.update()
      return jsonify({
        'success':True,
        'id':id
      })
    else:
      return jsonify({
        'success': False,
        'id':id
      })

  # this enpoint patches a new actor
  @app.route('/actors/<id>',methods=['PATCH'])
  @require_auth(permission='patch:actors')
  def edit_actor(id):
    actor_request = request.get_json()
    actor = Actors.query.get(id)

    if actor_request.get('name') is not None or actor_request.get('age') is not None or actor_request.get('gender') is not None:
      # determine the name
      if actor_request.get('name') is not None:
        actor.name = actor_request.get('name')
      # determine the age
      if actor_request.get('age') is not None:
        actor.age = actor_request.get('age')
      # determine the gender
      if actor_request.get('gender') is not None:
        actor.gender = actor_request.get('gender')
      # update
      actor.update()
      return jsonify({
        'success': True,
        'id':id
      })
    else:
      return jsonify({
        'success':False,
        'id':id
      })

    
  
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)