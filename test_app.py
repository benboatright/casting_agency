#9/10/22 #used this lesson to build this script #https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/fd1af4a3-5a8e-4d43-87cf-2467d773c1b8/concepts/092609e2-d972-4102-95c7-e78ba950bc2a
import os
import unittest
import json
from app import create_app
from models import setup_db, Actors, Movies
from flask_sqlalchemy import SQLAlchemy

#9/5/22 #referenced the code in the blog to hide secrets #https://dev.to/jakewitcher/using-env-files-for-environment%20#%20-variables-in-python-applications-55a1
from dotenv import load_dotenv
load_dotenv('.env')
test_url = os.getenv('test_url')

#using bearer tokens in unintest #https://knowledge.udacity.com/questions/316795
# use the Executive Producer Role to perform testing
exec_prod_token ='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZnR3RoZnp0ZnVfa05yUmpQQzVIciJ9.eyJpc3MiOiJodHRwczovL2Rldi1keTA4Nnowbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxNjUyN2ZiZGVhODBmYzY1ZWIxYTM3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MjgzMjMxNywiZXhwIjoxNjYyOTE4NzE3LCJhenAiOiJ6MWpQUE1QdHBteXlEbXJPRnNOc1JJSDdyZEhEZEQ5eCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.RyyYhStinEjaUHTVNQNPJu6R-LydGgKcAjYRjQbhO0HTyh4f60O3PqDFvNWTsDk7672t30O53l3vnrozwEdWt6Zs0yYrrDpPLoGcQ0g5MchL05eJp-y636UqBNTQzsc7wAVn_G-kEmTFdDPc2cGg4pqpoO1ezrEEZxWyGWgz2nFQOtmNXCDXidoSjyZheVN6l0EBnWPE6ib9DWxndoUA7jLzxk1A2ChDO21AcD4xQ7KDGToTg1DJxFSXoDAxCcJJP96KF7JdJgbMB_j2jw7Hx5qQr03giu0nGs2zYXA_TyPvu5Gxb_lxUhCWOTDmpxJ4zeIcdDzP1HpwFbmUTH5_Uw'

exec_producer_auth = {
    'Authorization': f'Bearer {exec_prod_token}'
}

class CastingAgencyTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = test_url
        setup_db(self.app,self.database_path)

    # failed get:movies
    def test_movie_error(self):
        res = self.client().get('/movies',headers=exec_producer_auth)
        self.assertEqual(res.status_code,404)
    # success get:movies
    def test_movie_success(self):
        new_movie = Movies(title='Top Gun 2',release_date='2022-05-27')
        new_movie.insert()
        res = self.client().get('/movies',headers=exec_producer_auth)
        self.assertEqual(res.status_code,200)
        
    
    # failed get:actors
    # success get:actors
    
    # failed post:movies
    # success post:movies

    # failed post:actors
    # success post:actors

    # failed patch:movies
    # success patch:movies

    # failed patch:actors
    # success patch:actors

    # failed delete:movies
    # success delete:movies

    # failed delete:actors
    # success delete:actors

if __name__ == "__main__":
    unittest.main()