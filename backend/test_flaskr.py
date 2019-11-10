import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from parameterized import parameterized

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        self.database_path =os.environ.get('DATABASE_URI_TEST')
        setup_db(self.app, self.database_path)

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass    

    def test_get_categories(self):
       num_categories = Category.query.count() 
       
       response = self.client.get('/categories')

       data = json.loads(response.data.decode())
       self.assertEqual(response.status_code, 200)
       self.assertTrue(isinstance(data['categories'], list))
       self.assertEqual(len(data['categories']), num_categories)


    def test_get_questions(self):
       num_questions = Question.query.count() 
       response = self.client.get('/questions')
       data = json.loads(response.data.decode())
       self.assertEqual(response.status_code, 200)
       self.assertTrue(isinstance(data['questions'], list))
       self.assertEqual(data['total_questions'], num_questions)

       self.assertTrue(isinstance(data['categories'], dict))

    def test_delete_question_with_invalid_id(self):
       response = self.client.delete(f'/questions/0')
       data = json.loads(response.data.decode())
       
       self.assertEqual(response.status_code, 404)
       self.assertEqual(data['message'],'Not Found' )

    def test_delete_question(self):
       question_id = Question.query.first().id 
       response = self.client.delete(f'/questions/{question_id}')
       data = json.loads(response.data.decode())
       
       self.assertEqual(response.status_code, 200)
       self.assertEqual(data['message'],'Question deleted successfully' )

       deleted_question = Question.query.get(question_id) 

       self.assertEqual(deleted_question, None)

    @parameterized.expand([
        ['', '', '', ''],
        ['answer', '', '', ''],
        ['answer', 'question', '', ''],
        ['answer', 'question', 1, ''],
        ['', '', '', 1],
        ['answer', 'question', 'answer', 'difficulty'],

    ])
    def test_create_question_with_invalid_data(self, answer, question, category, difficulty):
        question_input_data = {
            'answer': answer,
            'question': question,
            'category': category,
            'difficulty': difficulty
        }
        response = self.client.post(
            f'/questions',
             data=json.dumps(question_input_data), headers=self.headers)
        data = json.loads(response.data.decode())
       
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')
        self.assertEqual(data['error'], 400)

    def test_create_question_with_valid_data(self):
        question_input_data = {
            'answer': 'answer',
            'question': 'question',
            'category': 1,
            'difficulty': 1
        }

        response = self.client.post(
            f'/questions',
             data=json.dumps(question_input_data), headers=self.headers)
        data = json.loads(response.data.decode())
        question = data['question']
       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertEqual(question['question'], question_input_data['question'])
        self.assertEqual(question['answer'], question_input_data['answer'])
        self.assertEqual(question['category'], question_input_data['category'])
        self.assertEqual(question['difficulty'], question_input_data['difficulty'])
        self.assertIn('id', question.keys())


    def test_search_question_which_does_not_exist(self):
        response = self.client.post(
            f'/questions/search',
             data=json.dumps({'searchTerm': 'arthur'}), headers=self.headers)

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'],'Not Found' )
        self.assertFalse(data['success'])

    def test_search_question(self):
        question1 = Question(question='Is python a high level programming language', answer='answer2', difficulty=1, category=1)
        question2 = Question(question='True or False: Flask is a micro web framework written in Python', answer='answer342', difficulty=1, category=2)

        question1.insert()
        question2.insert()

        response = self.client.post(
            f'/questions/search',
             data=json.dumps({'searchTerm': 'python'}), headers=self.headers)

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(isinstance(data['questions'], list))
        self.assertEqual(data['total_questions'], 2)

        question1.delete()
        question2.delete()





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()