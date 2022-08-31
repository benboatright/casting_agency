import json
import os
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
        'success': 'True',
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
        'success' :'True',
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
        'success':'True',
        'id_deleted':id
      })
    # else, return the fail dictionary
    else:
      return jsonify({
        'success':'False',
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
        'success':'True',
        'id': id
      })
    # else, return the fail dictionary
    else:
      return jsonify({
        'success': 'False',
        'id': 'The id provided is not in the table'
      })


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)