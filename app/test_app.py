from multiprocessing.connection import answer_challenge
import os
from re import search
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from app import create_app
from database.models import setup_db, Actor, Movie

USER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJ3d0cwRUdNTWx4ZU5zb3o1b2JFTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1idTRnZWZmOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIxMDliYzQ5ZmYyYzYwMDY4ZWZmMWQ1IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2NDUyNjAwNzIsImV4cCI6MTY0NTI2NzI3MiwiYXpwIjoiWmh0ZGNGY01SWkJXc0tYZjNPMWtZS090d2RDblZXTzciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.Q49wU2sV6Ef9cmPUzD5YqgwEiTZ4If9v1jGN8RYrwUY6RPCwAuuOP3iSlpEcbEiLJfQJCHPTWCWetOEqdHiK_vwVsI-Cnoj5OsfLF_qpyP-pF07XiL3SelWAT4azl0dItcHIB78xsPgA029eK4H6t4RavzjVRVyqLQ4O-T5YTS271lcKaiJ_1jhS2_3Hioo7OkSyE7XinvXg5RHImZ_WHWfPZ06BYRb0cOpeDhA4oh-nlBx1B282Be9frTcQvdo_UJ0mc2lT1vFHv2wiyPfD6025v0wtq6vSNMStBouUZY2VX1XpWWYVH9666f_uvbrKK-amUephrkZbwwCrE61fXA"
ASSISTANT_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJ3d0cwRUdNTWx4ZU5zb3o1b2JFTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1idTRnZWZmOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIwZmQzNzFlMDhjM2QwMDZhNDhhMWFkIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2NDUyNjAwMDQsImV4cCI6MTY0NTI2NzIwNCwiYXpwIjoiWmh0ZGNGY01SWkJXc0tYZjNPMWtZS090d2RDblZXTzciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6YWN0b3JzLWRldGFpbCIsImdldDptb3ZpZXMiLCJnZXQ6bW92aWVzLWRldGFpbCJdfQ.VTgZiS_WK33KJOrrluLSOqqymo0o38Rc8bmj-s_BsL2N9n1T4QEnxx7YO_2mHYiENvwwFMgVzpTwcmUTCWC6GV5JW7Gy0Zf6Ra4e64QT6e7Oydg8Ol3qpn7SUyxn_Z9iQ1wPOdj04rxXECwVVudvM2QZBbVo_njiZK3eusFWMpZeBQ72AUOs3zNwn901-IONedFrovESjgyd-q8wjwdQMCx_Xi54_BC6zcwtQoCxpiy-xvnuKAyAvrcxBZ5uoTbgqNpzURjjbc1s_FwCPbaJsvoE_D7kYBneTuirP3FA-hPb7MAZX1N6FdMhj8rRihOHGMer7io5pWsmKbQ4JZ3jCA"
DIRECTOR_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJ3d0cwRUdNTWx4ZU5zb3o1b2JFTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1idTRnZWZmOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIwZmQzOTFjNDFmZjAwMDcyODUxMzJiIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2NDUyNTk5MzksImV4cCI6MTY0NTI2NzEzOSwiYXpwIjoiWmh0ZGNGY01SWkJXc0tYZjNPMWtZS090d2RDblZXTzciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6YWN0b3JzLWRldGFpbCIsImdldDptb3ZpZXMiLCJnZXQ6bW92aWVzLWRldGFpbCIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.sSeXiVjR-5L_FpQqvwInPpQhhscHNYqHFky1kOBTrF3IQwPVwavdWpzE0Py1PmNtwpNrj6EeEOPz9xTgF_CMBEgUNprjV5HKMmpbWdagZXsYweEoTmcV1S9BMLs5VbgdgFwQ3_NYoKv6NqDLND8-b8ImGFYbo_qtsOkPcAQuxpZj5ldelNX8NvIwoTtXKJ9dWgqIg1CQFGM55GIHCeVeXPrJSRlUhmu-3ZkSmwKaq1j7XkWU-ZzaSc0pyxIAFEBCAgx40V69hCyaCKy59Hi1iZlbX-mVefoqJ2iV9zul7R5Gq22j0Hw_Qrjkjri1i6VRNrkLF6WWkzB1FTM4Akl6UA"
PRODUCER_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJ3d0cwRUdNTWx4ZU5zb3o1b2JFTCJ9.eyJpc3MiOiJodHRwczovL2Rldi1idTRnZWZmOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjIwZmQzNDUxYjYzNWYwMDcwZWE1NTUwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2NDUyNTk4MzMsImV4cCI6MTY0NTI2NzAzMywiYXpwIjoiWmh0ZGNGY01SWkJXc0tYZjNPMWtZS090d2RDblZXTzciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6YWN0b3JzLWRldGFpbCIsImdldDptb3ZpZXMiLCJnZXQ6bW92aWVzLWRldGFpbCIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.DquIIJoZQbj8VpR9hgYnKDC1_OO6B-ogeXLWoMfiBC-lBw5v3vjw9iGSuK6-p4ZZFozNDbbYzcyixd7-jv_DIBNEDIs1rqx8vzwDlul0iOalgImSf39osXbNL6aemXInFq1Lj97dexeRzJneILB684GYTRvrVIwTR4JvbaRe1hbI4KAhPNMYxVeT_Yh5MCwciV8Fpfz0426xfBhugzZgotlz0hbeRctc6f9h_OwzbswiBnkYjwermvW-v4IRVUErSLqKOy-lIfnkwMvjmV4rz_gJ4aCXEQOfAvB4S49JPoCW_dCjHtjxiQb-zOtad7C_lg_I9X3zqLFC29B7AQWhDA"

USER_AUTH_HEADER = {'Authorization': f'Bearer {USER_TOKEN}'}
ASSISTANT_AUTH_HEADER = {'Authorization': f'Bearer {ASSISTANT_TOKEN}'}
DIRECTOR_AUTH_HEADER = {'Authorization': f'Bearer {DIRECTOR_TOKEN}'}
PRODUCER_AUTH_HEADER = {'Authorization': f'Bearer {PRODUCER_TOKEN}'}

class AgencyTestCase(unittest.TestCase):
    '''
    This class represents the agency test case
    '''

    def setUp(self):
        '''
        Define variables and initialize app
        '''
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # drop and create all tables
            self.db.drop_all()
            self.db.create_all()


    def tearDown(self):
        '''
        Executed after each test
        '''
        pass
    

    def test_get_actors_404(self):
        '''
        Tests Actors Loading Failure
        '''
        #Send request without inserting mock data
        res = self.client().get('/actors', headers=USER_AUTH_HEADER)
        data = json.loads(res.data)
    
        #Check status code, success, and message
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unauthorized")


    def test_get_actors(self):
        '''
        Tests Actors Loading Success
        '''

        #Insert a mock actor into db
        actor = Actor(name="Javier Bardem", age=55, gender="male")
        actor.insert()

        # Load Response Data
        res = self.client().get('/actors', headers=ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, success, existence of actors, and length of them
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))


    def test_get_actor_by_id(self):
        '''
        Tests Actors Loading by Id Success
        '''

        # Load Response Data
        res = self.client().get('/actors/1', headers=ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, success, existence of actor
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 1)


    def test_get_actor_by_id_404(self):
        '''
        Tests Actors Loading by Id Failure
        '''

        # Load Response Data
        res = self.client().get('/actors/123214123413', headers=ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, success, existence of actor
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")


    def test_create_new_actor(self):
        '''
        Test Actor Create Success
        '''
        new_actor = {
            "name": "Javier Bardem",
            "age": 55,
            "gender": "male"
        }

        # Send request to create a new actor
        res = self.client().post('/actors', json=new_actor, headers=PRODUCER_AUTH_HEADER)

        # Load response data
        data = json.loads(res.data)

        # Check status code, success, and actor
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], new_actor['name'])


    def create_new_actor_422(self):
        '''
        Test Actor Create Failure
        '''
        new_actor = {
            "name": "Javier Bardem",
            "age": 55
        }

        # Send request to create a new actor
        res = self.client().post('/actors', json=new_actor, headers=DIRECTOR_AUTH_HEADER)

        # Load response data
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


    def update_an_actor(self):
        '''
        Tests Actor Update Success
        '''
        actor = Actor.query.first()

        # Create update data
        actor_updated = {
            "name": "John Travolta"
        }
        # Send request and Load Response Data
        actor_id = actor.id
        res = self.client().patch('/actors/{actor_id}', json=actor_updated,
            headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, success, existence of actor
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor_updated['name'])
        self.assertEqual(data['actor']['age'], actor.age)
        self.assertEqual(data['actor']['gender'], actor.gender)

        actor_updated = Actor.query.get(data['actor']['id'])
        self.assertEqual(actor_updated.id, actor.id)


    def update_an_actor_404(self):
        '''
        Tests Actor Update Failure
        '''
        # Create update data
        actor_updated = {
            "name": "John Travolta"
        }
        # Send request and Load Response Data
        res = self.client().patch('/actors/9999999999', json=actor_updated,
            headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


    def delete_an_actor(self):
        '''
        Tests Actor Delete Success
        '''
        actor = Actor.query.first()

        # Send request and Load Response Data
        actor_id = actor.id
        res = self.client().delete('/actors/{actor_id}', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_actor']['id'], actor.id)


    def delete_an_actor_500(self):
        '''
        Tests Actor Delete Failure
        '''
        # Send request and Load Response Data
        res = self.client().delete('/actors/999999999', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['error'], 500)
        self.assertFalse(data['success'])


    def test_get_movies_404(self):
       '''
       Tests Movies Loading Failure
       '''
       #Send request without inserting mock data
       res = self.client().get('/movies', headers=USER_AUTH_HEADER)
       data = json.loads(res.data)
    
       #Check status code, success, and message
       self.assertEqual(res.status_code, 401)
       self.assertEqual(data['success'], False)
       self.assertEqual(data['message'], "Unauthorized")


    def test_get_movies(self):
        '''
        Tests Movies Loading Success
        '''

        #Insert a mock movie into db
        movie = Movie(name="No Country for Old Men", 
            release_year=2007, duration=123, genre="crime")
        movie.insert()

        # Load Response Data
        res = self.client().get('/movies', headers=ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, success, existence of movies, and length of them
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        movies = Movie.query.all()
        self.assertEqual(len(data['movies']), len(movies))


    def test_get_movie_by_id(self):
        '''
        Tests Movies Loading by Id Success
        '''

        # Load Response Data
        res = self.client().get('/movies/1', headers=ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, success, existence of movie
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 1)


    def test_get_movie_by_id_404(self):
        '''
        Tests Movies Loading by Id Failure
        '''

        # Load Response Data
        res = self.client().get('/movies/123214123413', headers=ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, success, existence of movie
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")


    def test_create_new_movie(self):
        '''
        Test Movie Create Success
        '''
        new_movie = {
            "name": "Saving Private Ryan",
            "release_year": 2000,
            "duration":220,
            "genre": "history"
        }

        # Send request to create a new movie
        res = self.client().post('/movies', json=new_movie, headers=PRODUCER_AUTH_HEADER)

        # Load response data
        data = json.loads(res.data)

        # Check status code, success, and movie
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['name'], new_movie['name'])


    def create_new_movie_422(self):
        '''
        Test Movie Create Failure
        '''
        new_movie = {
            "name": "Saving Private Ryan",
            "release_year": 2000
        }

        # Send request to create a new movie
        res = self.client().post('/movies', json=new_movie, headers=DIRECTOR_AUTH_HEADER)

        # Load response data
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


    def update_a_movie(self):
        '''
        Tests Movie Update Success
        '''
        movie = Movie.query.first()
        # Create update data
        movie_updated = {
            "name": "Letters from Iwo Jima"
        }
        # Send request and Load Response Data
        res = self.client().patch('/movies/{movie.id}', json=movie_updated,
            headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)
        movie = Movie.query.get(1)
        # Check status code, success, existence of movie
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['name'], movie_updated['name'])

        movie_updated = Movie.query.get(data['actor']['id'])
        self.assertEqual(movie_updated.id, movie.id)


    def update_an_movie_404(self):
        '''
        Tests Movie Update Failure
        '''
        # Create update data
        movie_updated = {
            "name": "Letters form Iwo Jima"
        }
        # Send request and Load Response Data
        res = self.client().patch('/movie/9999999999', json=movie_updated,
            headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


    def delete_a_movie(self):
        '''
        Tests Movie Delete Success
        '''
        movie = Movie.query.first()

        # Send request and Load Response Data
        res = self.client().delete('/movies/{movie.id}', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)
        movie = Movie.query.get(1)
        # Check status code, and success
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_movie']['id'], movie.id)


    def delete_an_movie_500(self):
        '''
        Tests Movie Delete Failure
        '''
        # Send request and Load Response Data
        res = self.client().delete('/movies/999999999', headers=PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['error'], 500)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()