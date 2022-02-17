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
    
    def test_get_actors(self):
        '''
        Tests Actors Loading Success
        '''

        #Insert a mock actor into db
        actor = Actor(name="Javier Bardem", age=55, gender="male")
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
        actor = Actor(name="Javier Bardem", age=55, gender="male")
        actor.insert()

        # Load Response Data
        actor = Actor.query.first()
        res = self.client().get('/actors/2')
        data = json.loads(res.data)

        # Check status code, success, existence of actor
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], actor.id)


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
        res = self.client().post('/actors', json=new_actor, headers={'Content-Type': 'application/json'})

        # Load response data
        data = json.loads(res.data)
        actor_added = Actor.query.get(data['actor']['id'])

        # Check status code, success, and actor
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], new_actor['name'])
        self.assertTrue(actor_added)


    def create_new_actor_422(self):
        '''
        Test Actor Create Failure
        '''
        new_actor = {
            "name": "Javier Bardem",
            "age": 55
        }

        # Send request to create a new actor
        res = self.client().post('/actors', json=new_actor, headers={'Content-Type': 'application/json'})

        # Load response data
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])


    def update_an_actor(self):
        '''
        Tests Actor Update Success
        '''
        #Insert a mock actor into db
        actor = Actor(name="Javier Bardem", age=55, gender="male")
        actor.insert()

        # Create update data
        actor_updated = {
            "name": "John Travolta"
        }
        # Send request and Load Response Data
        actor_id = actor.id
        res = self.client().patch('/actors/{actor_id}', json=actor_updated,
            headers={'Content-Type': 'application/json'})
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
            headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


    def delete_an_actor(self):
        '''
        Tests Actor Delete Success
        '''
        #Insert a mock actor into db
        actor = Actor(name="Javier Bardem", age=55, gender="male")
        actor.insert()

        # Send request and Load Response Data
        actor_id = actor.id
        res = self.client().delete('/actors/{actor_id}')
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
        res = self.client().delete('/actors/999999999')
        data = json.loads(res.data)

        # Check status code, and success
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['error'], 500)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()