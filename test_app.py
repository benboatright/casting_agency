# 9/10/22 #used this lesson to build this script
# #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/fd1af4a3-5a8e-4d43-87cf-2467d773c1b8/concepts/092609e2-d972-4102-95c7-e78ba950bc2a
# 9/10/22 #used the review code associated with this lesson to build this
# script as well
# #https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Review/backend/test_flaskr.py
from email import header
import os
import unittest
import json

from requests import delete
from app import create_app
from models import setup_db, Actors, Movies
from flask_sqlalchemy import SQLAlchemy

# 9/5/22 #referenced the code in the blog to hide secrets
# #https://dev.to/jakewitcher/using-env-files-for-environment%20#%20-variables-in-python-applications-55a1
from dotenv import load_dotenv
load_dotenv('.env')
test_url = os.getenv('test_url')

# 9/10/22 # learned how to use bearer tokens in unittest by referrencing
# the code linked #https://knowledge.udacity.com/questions/316795
exec_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZnR3RoZnp0ZnVfa05yUmpQQzVIciJ9.eyJpc3MiOiJodHRwczovL2Rldi1keTA4Nnowbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxNjUyN2ZiZGVhODBmYzY1ZWIxYTM3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MzE5NDc3NiwiZXhwIjoxNjYzMjgxMTc2LCJhenAiOiJ6MWpQUE1QdHBteXlEbXJPRnNOc1JJSDdyZEhEZEQ5eCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.PYDdlDijykF1v4yuZGGEbof7oYMM-BW02SoKcVIMh-9m4cJap7czBz_1_gN9QhxCEZ3c5fGytmQ73hqlMNaYGp6TET8cNj5OZvIaQiOFyK7nxdwZXMv1BzQTq15SKFQXobhLAptgxj_gfPSdzhqPZON-_3yoTVXc5efGjUxX9vx43qivGHjxvzfEA8OJELazrEVMDnxuE9DOzzbWxaEYJYIon1vvs5RJA5F2amz6324EQi_YYj1_iPp_Qo0mPcmRGTZsflB3eyDBf9HYmPjWGk-m3yknNbcKcoEalFDpmqfFcJV4DKirmREFaLmIw_AOJUUAD2PMcgt8ILuQrd-hqg'
cast_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZnR3RoZnp0ZnVfa05yUmpQQzVIciJ9.eyJpc3MiOiJodHRwczovL2Rldi1keTA4Nnowbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxNjUyNGVkZTgwZDg5Zjc3NzdlNGJiIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MzE5NDY5MiwiZXhwIjoxNjYzMjgxMDkyLCJhenAiOiJ6MWpQUE1QdHBteXlEbXJPRnNOc1JJSDdyZEhEZEQ5eCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.mVxePBB6JETZ9fhQulVVjD8qt8KxMNA769lKkgcmbIYd7M6L0rCAVojsd3YmaJ-uI8fmgONNhAqfu1FR-GiUHwsFseqrHVRRUY9pEk-AwGX9gFwx7OMoBqEAjR2BRibl-nwrBeUAsOaqke_3ts_tuGr2C4JEMKYWDXL4IAYQWJjC3x1VRwvKzrwQqatSIQ0x760sEjk9q8alTLfxLT63Aq46wcACQWXxy7JnH89jlE20Av33O1VjQJh8m6XousZPOe5Bss3SAh2q4ymolPnKBGp9mva72NIyVHjaKWC2_gvDn2OaJw493qx1abd1nTB17AxardtRm3KYIfa9bZ8b6g'
cast_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZnR3RoZnp0ZnVfa05yUmpQQzVIciJ9.eyJpc3MiOiJodHRwczovL2Rldi1keTA4Nnowbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxNjUyMGU3MmE0NWM1MDc4MTY4MTZmIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MzE5NDU2MCwiZXhwIjoxNjYzMjgwOTYwLCJhenAiOiJ6MWpQUE1QdHBteXlEbXJPRnNOc1JJSDdyZEhEZEQ5eCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.duMfVaJ0uAQtIJfYQGwxKLKbU1Qgd53gUUm8I1JMDvw76hYAf7Bt96W63apKT8Z2UTM5NeFmLdGFO3K3u0OYiRGm8Bf79POlKdwjAsFULfUfVHNWyhdK_VmQu3g4jaqfQI1TJyPSeorZUtXPw7A6od04sEFSQbGYzMZt_FOZqdElw7UnvPm15wqjF9tF7jV2GzyEyjgL1L61xC8-Ndj39EvpokXcqDzHpM1EzQjTVxvAAA9vjW8Hi8KYx0gDkWB1CphOBbNZHj9fWiX-mTvJl_36jivRQeaDkWuPvCjgmzYTs10yBIXTFaHovRKAe4z9fFbCbn24U7TZ4A3YZtqluw'

exec_producer_auth = {'Authorization': f'Bearer {exec_producer_token}'}
cast_director_auth = {'Authorization': f'Bearer {cast_director_token}'}
cast_assistant_auth = {'Authorization': f'Bearer {cast_assistant_token}'}


class CastingAgencyTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = test_url
        setup_db(self.app, self.database_path)

    # failed get:movies
    def test_get_movie_error(self):
        # since the table is empty, test that it returns 404
        res = self.client().get('/movies', headers=exec_producer_auth)
        self.assertEqual(res.status_code, 404)

    # success get:movies
    def test_get_movie_success(self):
        # add movies for testing
        new_movie = Movies(
            title='Top Gun: Maverick',
            release_date='2022-05-27')
        new_movie.insert()
        # access endpoint
        res = self.client().get('/movies', headers=exec_producer_auth)
        data = json.loads(res.data)
        # run tests
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['title'], 'Top Gun: Maverick')
        # clear out the added data
        delete_movie = Movies.query.all()
        for movie in delete_movie:
            movie.delete()

    # failed get:actors
    def test_get_actors_error(self):
        res = self.client().get('/actors', headers=exec_producer_auth)
        self.assertEqual(res.status_code, 404)

    # success get:actors
    def test_get_actors_succes(self):
        # add an actor for testing the get endpoint
        new_actor = Actors(name='Tom Cruise', age=60, gender='Male')
        new_actor.insert()
        # access the endpoint
        res = self.client().get('/actors', headers=exec_producer_auth)
        data = json.loads(res.data)
        # run the test
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]['name'], 'Tom Cruise')
        # delete the added data
        delete_actor = Actors.query.all()
        for actor in delete_actor:
            actor.delete()

    # failed post:movies
    def test_post_movies_error(self):
        # create json data for the post
        new_movie = {
            'screen_name': 'Top Gun: Maverick',
            'release': '2022-05-27'
        }
        # access the endpoint and attempt post request
        res = self.client().post('/movies',
                                 headers=exec_producer_auth,
                                 json=new_movie)
        # the column names are incorrect, so this returns 400 error
        self.assertEqual(res.status_code, 400)

    # success post:movies
    def test_post_movies_success(self):
        # create json data for the post
        new_movie = {
            'title': 'Top Gun: Maverick',
            'release_date': '2022-05-27'
        }
        # attempt post request
        res = self.client().post('/movies',
                                 headers=exec_producer_auth,
                                 json=new_movie)
        # get the data from the response
        data = json.loads(res.data)
        # check that it worked
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['title'], 'Top Gun: Maverick')
        # delete the data
        delete_movies = Movies.query.all()
        for movie in delete_movies:
            movie.delete()

    # failed post:actors
    def test_post_actors_error(self):
        # create an actor for testing
        new_actor = {
            'full_name': 'Tom Cruise',
            'age': 60,
            'gender': 'Male'
        }
        # attempt to access endpoint
        res = self.client().post('/actors',
                                 headers=exec_producer_auth,
                                 json=new_actor)
        # the response should be 400 because full_name is not the column name
        self.assertEqual(res.status_code, 400)

    # success post:actors
    def test_post_actors_success(self):
        # create new actor
        new_actor = {
            'name': 'Tom Cruise',
            'age': 60,
            'gender': 'Male'
        }
        # attepmt the post request
        res = self.client().post('/actors',
                                 headers=exec_producer_auth,
                                 json=new_actor)
        # retreive the data
        data = json.loads(res.data)
        # the post request should be succesfull and add the actor
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['name'], 'Tom Cruise')
        # delete the actor from the database
        delete_actors = Actors.query.all()
        for actor in delete_actors:
            actor.delete()

    # failed patch:movies
    def test_patch_movies_error(self):
        # add new movie
        new_movie = Movies(
            title='Top Gun: Maverick',
            release_date='1986-05-16')
        new_movie.insert()
        # try to update this movie's release date
        update_movie = {
            'release_date': '2020-05-27'
        }
        patched_movie = Movies.query.all()
        movie_id = patched_movie[0].id
        # change the id to create the 404 error since the id does not exist
        wrong_movie_id = movie_id + 1
        # attempt the patch request
        res = self.client().patch(
            f'/movies/{wrong_movie_id}',
            headers=exec_producer_auth,
            json=update_movie)
        self.assertEqual(res.status_code, 404)
        # delete the movie
        delete_movies = Movies.query.all()
        for movie in delete_movies:
            movie.delete()

    # success patch:movies
    def test_patch_movies_success(self):
        new_movie = Movies(
            title='Top Gun: Maverick',
            release_date='1986-05-16')
        new_movie.insert()
        update_movie = {
            'release_date': '2020-05-27'
        }
        patched_movie = Movies.query.all()
        movie_id = patched_movie[0].id
        # attempt the patch request with the correct
        res = self.client().patch(
            f'/movies/{movie_id}',
            headers=exec_producer_auth,
            json=update_movie)
        data = json.loads(res.data)
        # perform the test to make sure the patch was successful
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(data['id']), movie_id)
        # delete the movie from the table
        delete_movies = Movies.query.all()
        for movie in delete_movies:
            movie.delete()

    # failed patch:actors
    def test_patch_actors_error(self):
        # add an actress to the table
        new_actress = Actors(name='Jennifer Connelly', age=50, gender='Female')
        new_actress.insert()
        # attempt to update the age with new json
        update_actress = {
            'age': 51
        }
        # get the id for the patch request
        patched_actress = Actors.query.all()
        actress = patched_actress[0]
        actress_id = actress.id
        # change the id so that it does not exist. This will cause 404 error
        wrong_actress_id = actress_id + 1
        # attempt to make the patch request
        res = self.client().patch(
            f'/actors/{wrong_actress_id}',
            headers=exec_producer_auth,
            json=update_actress)
        # the patch should fail becuase the column name is incorrect
        self.assertEqual(res.status_code, 404)
        # delete the actress from the database
        delete_actors = Actors.query.all()
        for actors in delete_actors:
            actors.delete()

    # success patch:actors
    def test_patch_actors_success(self):
        # add a new actress to the table
        new_actress = Actors(name='Jennifer Connelly', age=50, gender='Female')
        new_actress.insert()
        # update the age with a new json update
        update_actress = {
            'age': 51
        }
        # get the id of the actor for the patch
        patched_actress = Actors.query.all()
        actress = patched_actress[0]
        actress_id = actress.id
        # test the patch request
        res = self.client().patch(
            f'/actors/{actress_id}',
            headers=exec_producer_auth,
            json=update_actress)
        data = json.loads(res.data)
        # make sure it worked
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # delete the actress from the table
        delete_actors = Actors.query.all()
        for actor in delete_actors:
            actor.delete()

    # failed delete:movies
    def test_delete_movies_error(self):
        # create a movie to delete
        new_movie = Movies(
            title='Top Gun: Maverick',
            release_date='2022-05-27')
        new_movie.insert()
        # get the wrong id for delete to fail 404
        movies = Movies.query.all()
        movie_id = movies[0].id
        wrong_id = movie_id + 1
        # attempt the delete request
        res = self.client().delete(
            f'/movies/{wrong_id}',
            headers=exec_producer_auth)
        self.assertEqual(res.status_code, 404)
        # delete movies for other test to work
        delete_movies = Movies.query.all()
        for movie in delete_movies:
            movie.delete()

    # success delete:movies
    def test_delete_movies_success(self):
        # create a move to delete
        new_movie = Movies(
            title='Top Gun: Maverick',
            release_date='2022-05-27')
        new_movie.insert()
        # get the right id for delete success
        movies = Movies.query.all()
        movie_id = movies[0].id
        # attempt the delete request
        res = self.client().delete(
            f'/movies/{movie_id}',
            headers=exec_producer_auth)
        data = json.loads(res.data)
        # test that the delete was successful
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(data['id']), movie_id)
        # delete the movie
        delete_movies = Movies.query.all()
        for movie in delete_movies:
            movie.delete()

    # failed delete:actors
    def test_delete_actors_error(self):
        # create an actress for delete
        new_actress = Actors(name='Jennifer Connelly', age=51, gender='Female')
        new_actress.insert()
        # get the correct id for delete
        actress = Actors.query.all()
        actress_id = actress[0].id
        # make the id wrong, causing a 404 error
        wrong_id = actress_id + 100
        # attempt the delete
        res = self.client().delete(
            f'/actors/{wrong_id}',
            headers=exec_producer_auth)
        # test the failure
        self.assertEqual(res.status_code, 404)
        # delete the actress from table
        delete_actors = Actors.query.all()
        for actor in delete_actors:
            actor.delete()

    # success delete:actors
    def test_delete_actors_success(self):
        # insert new actress to delete
        new_actress = Actors(name='Jennifer Connelly', age=51, gender='Female')
        new_actress.insert()
        # find the right id
        actress = Actors.query.all()
        actress_id = actress[0].id
        # make the delete request
        res = self.client().delete(
            f'/actors/{actress_id}',
            headers=exec_producer_auth)
        data = json.loads(res.data)
        # check to make sure it was successfully deleted
        self.assertEqual(res.status_code, 200)
        self.assertEqual(int(data['id']), actress_id)
        # delete the actress
        delete_actors = Actors.query.all()
        for actor in delete_actors:
            actor.delete()

    # Casting Assistant Success on Get Request
    def test_casting_assistant_success_get(self):
        # add an actor for the casting assistant to view
        new_actor = Actors(name='Tom Cruise', age=60, gender='Male')
        new_actor.insert()
        # attempt the get request
        res = self.client().get('/actors', headers=cast_assistant_auth)
        self.assertEqual(res.status_code, 200)

    # Casting Assistant Failure on Post Request
    def test_casting_assistant_error_post(self):
        # try to post the new actor below, but this should fail based on RBAC
        new_actor = {
            'name': 'Tom Cruise',
            'age': 60,
            'gender': 'Male'
        }
        res = self.client().post('/actors',
                                 headers=cast_assistant_auth,
                                 json=new_actor)
        # test that this should fail
        self.assertEqual(res.status_code, 403)
        # delete the actor
        delete_actors = Actors.query.all()
        for actor in delete_actors:
            actor.delete()

    # Casting Director Success on Post Actor
    def test_casting_director_success_post_actor(self):
        # new actor to post
        new_actor = {
            'name': 'Tom Cruise',
            'age': 60,
            'gender': 'male'
        }
        # attempt the post
        res = self.client().post('/actors',
                                 headers=cast_director_auth,
                                 json=new_actor)
        # test the results that should pass
        self.assertEqual(res.status_code, 200)
        # delete the actor
        delete_actors = Actors.query.all()
        for actor in delete_actors:
            actor.delete()

    # Casting Director Failure on Post Movie
    def test_casting_director_failure_post_movie(self):
        new_movie = {
            'title': 'Top Gun: Maverick',
            'release_date': '2022-05-27'
        }
        # attempt to post new movie
        res = self.client().post('/movies',
                                 headers=cast_director_auth,
                                 json=new_movie)
        # this should fail because the casting director does not have this
        # permission
        self.assertEqual(res.status_code, 403)
        # delete the movies
        delete_movies = Movies.query.all()
        for movie in delete_movies:
            movie.delete()

    # Executive Producer Success on Post Movie
    def test_exec_producer_success_post_movie(self):
        new_movie = {
            'title': 'Top Gun: Maverick',
            'release_date': '2022-05-27'
        }
        # post the new movie
        res = self.client().post('/movies',
                                 headers=exec_producer_auth,
                                 json=new_movie)
        # This will pass with 200 code
        self.assertEqual(res.status_code, 200)
        # delete the movie
        delete_movies = Movies.query.all()
        for movie in delete_movies:
            movie.delete()

    # Executive Producer Success on Delete Movie
    def test_exec_producer_success_delete_movie(self):
        # add a movie to be deleted
        new_movie = Movies(
            title='Top Gun: Maverick',
            release_date='2022-05-27')
        new_movie.insert()
        # find the id of the movie
        movies = Movies.query.all()
        movie_id = movies[0].id
        # attempt the delete request
        res = self.client().delete(
            f'/movies/{movie_id}',
            headers=exec_producer_auth)
        # this should pass because the exec producer is allowed to delete
        # movies
        self.assertEqual(res.status_code, 200)
        # delete the movies
        delete_movies = Movies.query.all()
        for movie in delete_movies:
            movie.delete()


if __name__ == "__main__":
    unittest.main()
