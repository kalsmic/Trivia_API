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
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_path = os.environ.get("DATABASE_URI")
        setup_db(self.app, self.database_path)

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
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

        response = self.client.get("/categories")

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data["categories"], dict))
        self.assertEqual(len(data["categories"]), num_categories)

    def test_get_questions(self):
        num_questions = Question.query.count()
        response = self.client.get("/questions")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data["questions"], list))
        self.assertEqual(data["total_questions"], num_questions)

    def test_delete_question_with_invalid_id(self):
        response = self.client.delete(f"/questions/0")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Not Found")

    def test_delete_question(self):
        question_id = Question.query.first().id
        response = self.client.delete(f"/questions/{question_id}")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Question deleted successfully")

        deleted_question = Question.query.get(question_id)

        self.assertEqual(deleted_question, None)

    #
    @parameterized.expand(
        [
            ["", "", "", ""],
            ["answer", "", "", ""],
            ["answer", "question", "", ""],
            ["answer", "question", 1, ""],
            # ["", "", "", 1],
            ["answer", "question", "answer", "difficulty"],
        ]
    )
    def test_create_question_with_invalid_data(
        self, answer, question, category, difficulty
    ):
        question_input_data = {
            "answer": answer,
            "question": question,
            "category": category,
            "difficulty": difficulty,
        }
        response = self.client.post(
            f"/questions",
            data=json.dumps(question_input_data),
            headers=self.headers,
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")
        self.assertEqual(data["error"], 400)

    def test_create_question_with_valid_data(self):
        question_input_data = {
            "answer": "answer",
            "question": "question",
            "category": 1,
            "difficulty": 1,
        }

        response = self.client.post(
            f"/questions",
            data=json.dumps(question_input_data),
            headers=self.headers,
        )
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

        question = data["question"]

        self.assertEqual(question["question"], question_input_data["question"])
        self.assertEqual(question["answer"], question_input_data["answer"])
        self.assertEqual(question["category"], 1)
        self.assertEqual(
            question["difficulty"], question_input_data["difficulty"]
        )
        self.assertIn("id", question.keys())

    def test_search_question_which_does_not_exist(self):
        response = self.client.post(
            "/questions/search",
            data=json.dumps({"searchTerm": "arthur"}),
            headers=self.headers,
        )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "Not Found")
        self.assertFalse(data["success"])

    def test_search_question(self):
        question1 = Question(
            question="True or False: Django is a high-level Python Web"
                     " framework that encourages rapid development"
                     " and clean, pragmatic design",
            answer="True",
            difficulty=1,
            category=1,
        )
        question2 = Question(
            question="True or False: django is a micro web framework "
                     "written in Python",
            answer="False",
            difficulty=1,
            category=2,
        )

        question1.insert()
        question2.insert()

        response = self.client.post(
            "/questions/search",
            data=json.dumps({"searchTerm": "django"}),
            headers=self.headers,
        )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(isinstance(data["questions"], list))
        self.assertEqual(data["total_questions"], 2)

        question1.delete()
        question2.delete()

    def test_get_question_by_category_with_invalid_category_id(self):
        response = self.client.get("categories/0/questions")
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Not Found")

    def test_get_question_by_category(self):
        question1 = Question(
            question="Is python a high level programming language",
            answer="answer2",
            difficulty=1,
            category=2,
        )
        question1.insert()

        response = self.client.get("categories/2/questions")
        data = json.loads(response.data.decode())

        num_questions = Question.query.filter_by(category=2).count()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["total_questions"], num_questions)
        self.assertEqual(data["current_category"], 2)

        question1.delete()

    def test_get_quizzes_only_returns_question_not_in_previous_question(self):

        previous_questions = [question.id for question in Question.query.all()]

        question1 = Question(
            question="Is python a high level programming language",
            answer="answer2",
            difficulty=1,
            category=1,
        )
        question1.insert()

        response = self.client.post(
            "/quizzes",
            data=json.dumps(
                {
                    "previous_questions": previous_questions,
                    "quiz_category": {"id": "1"},
                }
            ),
            headers=self.headers,
        )
        data = json.loads(response.data.decode())
        question = data["question"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(question["id"], question1.id)
        self.assertEqual(question["answer"], question1.answer)
        self.assertEqual(question["question"], question1.question)
        self.assertEqual(question["difficulty"], question1.difficulty)
        self.assertEqual(question["category"], question1.category)
        self.assertEqual(question["category"], 1)

        question1.delete()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
