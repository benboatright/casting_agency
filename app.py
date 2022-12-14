import json
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# 9/5/22 # referenced this code to remember how to perform authorizations
# https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
from urllib.request import urlopen
# 9/5/22 #referenced this code to remember how to perform authorizations
# https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
from jose import jwt
# 9/5/22 #referenced this code to remember how to perform authorizations
# https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
from functools import wraps
from models import setup_db, Actors, Movies
# 9/5/22 #referenced the code in the blog to hide secrets
# #https://dev.to/jakewitcher/using-env-files-for-environment%20#%20-variables-in-python-applications-55a1
from dotenv import load_dotenv
load_dotenv('.env')
# had to downgrade flask and flask migrate and other versions to match the
# sample requirements# https://knowledge.udacity.com/questions/722150

# how to generate new sign ins / tokens
# https://dev-dy086z0n.us.auth0.com/authorize?audience=casting&response_type=token&client_id=z1jPPMPtpmyyDmrOFsNsRIH7rdHDdD9x&redirect_uri=http://localhost:8080/login-results

# user_name = os.getenv('user_name')
database_url = os.environ['DATABASE_URL']  # os.getenv('database')
domain = os.environ['DOMAIN']  # os.getenv('auth_domain')
api = os.environ['API']  # os.getenv('api')

# uri = f'postgresql://{user_name}@{database}' #8/29/22 #Referenced Amy's
# lesson on connecting to the database
# #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/b2093f89-9b28-4d97-a02c-a829315fd3e1
# 8/29/22 #Referenced Amy's lesson on connecting to the database
# https://learn.udacity.com/nanodegrees/nd0044/parts/cd0046/lessons/b957ba99-1c62-471c-8482-c18ac3d7943b/concepts/b2093f89-9b28-4d97-a02c-a829315fd3e1
uri = f'{database_url}'

# Authorization Methods
# 9/5/22 #referenced this code to build the retreive token function
# https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py
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
# 9/5/22 #referenced this code to build the verify and decode function
# #https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py


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
        # if the 'kid' from one of the keys matches the 'kid from the
        # unverified header, populate the rsa_key dictionary
        if key['kid'] == unver_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # if the rsa_key was populated try to decode and return the payload
    if rsa_key is not None:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=['RS256'],
                audience=api,
                issuer=f'https://{domain}/')
            return payload
        except BaseException:
            abort(401)

# Build the require_authorization method
# 9/5/22 #referenced this code to build the check permissions function
# #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/1e1c8e9d-61af-4a0a-b7d5-87e5becf9be7/concepts/b4d79d5c-3d79-43e6-93ca-0d750043a373


def check_perms(permission, payload):
    if permission not in payload['permissions']:
        abort(403)
    else:
        return True

# 9/5/22 #referenced this code to build the require auth method
# #https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py


def require_auth(permission=''):
    def require_authorization_decor(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # retreive the token
            token = retreive_token()
            try:
                # get the payload using the ver_and_decode_jwt method and the
                # token
                payload = ver_and_decode_jwt(token)
            except BaseException:
                abort(401)
                # make sure that the payload included the permission associated
                # with a given endpoint
            # 9/5/22 #referenced this code to add in permissions
            # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/1e1c8e9d-61af-4a0a-b7d5-87e5becf9be7/concepts/b4d79d5c-3d79-43e6-93ca-0d750043a373
            check_perms(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return require_authorization_decor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app, uri)
    CORS(app)

    @app.route('/', methods=['GET'])
    def homepage():
        return 'Casting Agency API.'

    @app.route('/initialize', methods=['GET'])
    def initialize_tables():
        all_actors = Actors.query.all()
        tom_check = 0
        jennifer_check = 0
        for actor in all_actors:
            if actor.name == 'Tom Cruise':
                tom_check += 1
            if actor.name == 'Jennifer Connelly':
                jennifer_check += 1
        if tom_check == 0:
            new_actor = Actors(name='Tom Cruise', age=60, gender='Male')
            new_actor.insert()
        if jennifer_check == 0:
            new_actress = Actors(
                name='Jennifer Connelly',
                age=51,
                gender='Female')
            new_actress.insert()

        all_movies = Movies.query.all()
        top_gun_check = 0
        for movie in all_movies:
            if movie.title == 'Top Gun: Maverick':
                top_gun_check += 1
        if top_gun_check == 0:
            new_movie = Movies(
                title='Top Gun: Maverick',
                release_date='2022-05-27')
            new_movie.insert()
        return 'The "actors" table and the "movies" table has been initialized'

    # this endpoint gets all the movies form the data table
    @app.route('/movies', methods=['GET'])
    @require_auth(permission='get:movies')
    def get_movies(payload):
        # query all the movies from the table
        all_movies = Movies.query.all()
        # check if any movies
        if len(all_movies) == 0:
            abort(404)
        else:
            # initialize a list to store the movies
            movies_list = []
            # for each movie in the table,
            # create a dictionary with success,
            # id, title, and release date.
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
    @app.route('/actors', methods=['GET'])
    @require_auth(permission='get:actors')
    def get_actors(payload):
        # query all the actors from the table
        all_actors = Actors.query.all()
        # check if any actors
        if len(all_actors) == 0:
            abort(404)
        else:
            # init a list to hold the actors
            actors_list = []
            # for each actor in the table,
            # fill out a dictionary with success,
            # id, name, age, and gender.
            # then append each of the dictionaries to the list
            for actor in all_actors:
                actor_dict = {
                    'success': True,
                    'id': actor.id,
                    'name': actor.name,
                    'age': actor.age,
                    'gender': actor.gender
                }
                actors_list.append(actor_dict)
            # return the list
            return jsonify(actors_list)

    # this endpoint deletes a movie from the table based in the <id> passed in
    # the route handler
    @app.route('/movies/<id>', methods=['DELETE'])
    @require_auth(permission='delete:movies')
    def delete_movie(payload, id):
        # query the movie with the id from the route handler
        movie = Movies.query.get(id)
        # if the movie id is in the table, delete it and return the success
        # dictionary
        if movie is not None:
            movie.delete()
            return jsonify({
                'success': True,
                'id': id
            })
        # else, return the fail dictionary
        else:
            abort(404)

    # this endpoint deletes an actor from the table based on the <id> passed
    # in teh route handler
    @app.route('/actors/<id>', methods=['DELETE'])
    @require_auth(permission='delete:actors')
    def delete_actor(payload, id):
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
            abort(404)

    # this endpoint posts a new movie to the table based on the request made
    @app.route('/movies', methods=['POST'])
    @require_auth(permission='post:movies')
    def add_movie(payload):
        # 8/31/22 #Referenced Caryn's code to remember how to get the request
        # https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
        movie = request.get_json()
        # 8/31/22 #Referenced Caryn's code to remember how to get the request
        # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
        if movie.get('title') is not None and movie.get(
                'release_date') is not None:
            # 8/31/22 #Referenced Caryn's code to remember how to get the
            # request
            # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
            new_movie = Movies(
                title=movie.get('title'),
                release_date=movie.get('release_date'))
            new_movie.insert()
            return jsonify({
                'success': True,
                # 8/31/22 #Referenced Caryn's code to remember how to get the
                # request
                # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
                'title': movie.get('title'),
                # 8/31/22 #Referenced Caryn's code to remember how to get the
                # request
                # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
                'release_date': movie.get('release_date')
            })
        else:
            abort(400)

    # this endpoint posts a new actor to the table based on teh request
    @app.route('/actors', methods=['POST'])
    @require_auth(permission='post:actors')
    def add_actors(payload):
        # 8/31/22 #Referenced Caryn's code to remember how to get the request
        # https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
        actor = request.get_json()
        # 8/31/22 #Referenced Caryn's code to remember how to get the request
        # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
        if actor.get('name') is not None and actor.get(
                'age') is not None and actor.get('gender') is not None:
            # 8/31/22 #Referenced Caryn's code to remember how to get the
            # request
            # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
            new_actor = Actors(
                name=actor.get('name'),
                age=actor.get('age'),
                gender=actor.get('gender'))
            new_actor.insert()
            return jsonify({
                'success': True,
                # 8/31/22 #Referenced Caryn's code to remember how to get the
                # request
                # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
                'name': actor.get('name'),
                # 8/31/22 #Referenced Caryn's code to remember how to get the
                # request
                # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
                'age': actor.get('age'),
                # 8/31/22 #Referenced Caryn's code to remember how to get the
                # request
                # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/4cecb5bf-6b5c-4c5c-8428-51c49374bab0
                'gender': actor.get('gender')
            })
        else:
            abort(400)

    # this endpoint patches a new movie
    @app.route('/movies/<id>', methods=['PATCH'])
    @require_auth(permission='patch:movies')
    def edit_movie(payload, id):
        movie_request = request.get_json()
        movie = Movies.query.get(id)
        if movie is None:
            abort(404)

        if movie_request.get('title') is not None or movie_request.get(
                'release_date') is not None:
            # determine the title to update
            if movie_request.get('title') is not None:
                movie.title = movie_request.get('title')
            # determine the release date to update
            if movie_request.get('release_date') is not None:
                movie.release_date = movie_request.get('release_date')
            # make the update
            movie.update()
            return jsonify({
                'success': True,
                'id': id
            })
        else:
            abort(400)

    # this enpoint patches a new actor
    @app.route('/actors/<id>', methods=['PATCH'])
    @require_auth(permission='patch:actors')
    def edit_actor(payload, id):
        actor_request = request.get_json()
        actor = Actors.query.get(id)
        if actor is None:
            abort(404)

        if actor_request.get('name') is not None or actor_request.get(
                'age') is not None or actor_request.get('gender') is not None:
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
                'id': id
            })
        else:
            abort(400)

    # ERROR HANDLERS
    # 9/10/22 # used the linked video to build all these handlers
    # #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/905d1c8e-34d6-4d06-aaee-8ee91f041bc2/concepts/8755536a-7966-476b-81ac-063db44c85d4
    @app.errorhandler
    def resource_not_found():
        return jsonify({
            'success': False,
            'error code': 404,
            'error message': 'The resource you requested was not found.'
        }), 404

    @app.errorhandler
    def forbidden_request():
        return jsonify({
            'success': False,
            'error code': 403,
            'error message': 'You do not have permission to \
              access the resource you requested.'
        }), 403

    @app.errorhandler
    def unauthorized_request():
        return jsonify({
            'success': False,
            'error code': 401,
            'error message': 'You must be authenticated to\
               access this resource.'
        }), 401

    @app.errorhandler
    def bad_request():
        return jsonify({
            'success': False,
            'error code': 400,
            'error message': 'Syntax of the request was not understood.'
        })

    return app


app = create_app()

if __name__ == '__main__':
    app.run()  # (host='0.0.0.0', port=8080, debug=True)
