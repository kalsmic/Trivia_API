import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        self.database_name = "trivia_test"
        self.database_username = "postgres"
        self.database_password = "root"

        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = f"postgres://{self.database_username}:{self.database_password}@localhost:5432/trivia_test"


        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
       response = self.client.get('/questions')
       data = json.loads(response.data.decode())
       self.assertEqual(response.status_code, 200)
       self.assertTrue(isinstance(data['questions'], list))
       self.assertTrue(isinstance(data['categories'], list))


    #    assert qn.status == 200


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()