import json
import os
from platform import release
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db,Actors,Movies

uri = f'postgresql://benjaminboatright@localhost:5432/casting_agency' #8/29/22 #Referenced Amy's lesson on connecting to the database #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/b2093f89-9b28-4d97-a02c-a829315fd3e1

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app,uri)

  @app.route('/')
  def test():
    return 'Casting Agency'

  # this endpoint gets all the movies form the data table
  @app.route('/movies',methods=['GET'])
  def get_movies():
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