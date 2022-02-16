from multiprocessing.connection import answer_challenge
import os
from re import search
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from app import create_app
from database.models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):
    '''
    This class represents the agency test case
    '''

    def setUp(self):
        '''
        Define variables and initialize app
        '''
        self.user_auth_token = os.environ['user_auth_token']
        self.admin_auth_token = os.environ['admin_auth_token']
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://{}@{}/{}".format("postgres", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = sqlalchemy()
            self.db.init_app(self.app)
            # drop and create all tables
            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        '''
        Executed after each test
        '''
        pass
    
    def test_get_actors(self):
        '''
        Tests Actors Loading Success
        '''

        #Insert a mock actor into db
        actor = Actor(name="Javier Bardem", age="55", gender="male")
        actor.insert()

        # Load Response Data
        res = self.client().get('/actors')
        data = json.loads(res.data)

        # Check status code, success, existence of actors, and length of them
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_get_actors_404(self):
        '''
        Tests Actors Loading Failure
        '''
        #Send request without inserting mock data
        res = self.client().get('/categories')
        data = json.loads(res.data)

        #Check status code, success, and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")

    def test_get_actor_by_id(self):
        '''
        Tests Actors Loading by Id Success
        '''
        #Insert a mock actor into db
        actor = Actor(name="Javier Bardem", age="55", gender="male")
        actor.insert()

        # Load Response Data
        actor_id = actor.id
        res = self.client().get('/actors/{actor_id}')
        data = json.loads(res.data)

        # Check status code, success, existence of actor
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor'].id, actor.id)

    def test_get_actor_by_id_404(self):
        '''
        Tests Actors Loading by Id Failure
        '''

        # Load Response Data
        res = self.client().get('/actors/123214123413')
        data = json.loads(res.data)

        # Check status code, success, existence of actor
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Not Found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()