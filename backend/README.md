[![Build Status](https://travis-ci.org/kalsmic/Trivia_API.svg?branch=master)](https://travis-ci.org/kalsmic/Trivia_API)

[![Coverage Status](https://coveralls.io/repos/github/kalsmic/Trivia_API/badge.svg?branch=master)](https://coveralls.io/github/kalsmic/Trivia_API?branch=master)

# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions'
POST 'questions/search'
GET '/categories/<ind: category_id>/questions'
POST '/quizzes'
```

##### GET '/categories'
```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{"1":Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

##### GET '/questions'
```
- Fetches a list of paginated questions, and the total number of questions
- Request Arguments: page, set to one by default
- Returns: A list of questions and the total number of questions. 
{
    "questions":[
        {
          "answer": "Maya Angelou", 
          "category": 4, 
          "difficulty": 2, 
          "id": 5, 
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },{...},
    ],
    "total_questions": 20
}
- Returns 404 on error, when no questions are available or invalid page param is provided
{
  "error": 404, 
  "message": "Not Found", 
  "success": false
}
```


##### POST '/questions'
```
- Creates a new questiion
- Request Body: question to be created
{
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "question": "Whose automiography is entitled 'I Know Why the Caged Bird Sings'?"
     
}

- Returns: The newly created question. 

{
  "question": {
    "answer": "Maya Angelou",
    "category": 4,
    "difficulty": 2,
    "id": 26,
    "question": "Whose automiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  "success": true
}

- Returns 400 on error, when bad format data is provided
{
  "error": 400, 
  "message": "Bad Request", 
  "success": false
}
```

##### DELETE '/questions/<int:question_id>'
```
- Delete a question with specified id
- Request Arguments: question_id, the id of the question to delete
- Returns success message on success
{
  "message": "Question deleted successfully",
  "success": true
}
- Returns 404 on error
{
  "error": 404,
  "message": "Not Found",
  "success": false
}
```

##### POST '/questions/search'
```
- Search a question
- Request Body: searchTerm
{"searchTerm": "search term"}
- Returns success message on success
{
    "questions": [{...question}],
    "total_questions": "number_of_results",
    "success": true
}
- Returns 404 on error
{
  "error": 404,
  "message": "Not Found",
  "success": false
}
```

##### GET '/categories/<ind: category_id>/questions'
```
- Get questions of specified category id
- Returns a list of questions od the specified category
 {
    "questions": [{...question}, {...}],
    "total_questions": num_of_questions,
    "current_category": category_id,
}
- Returns 404 on error
{
  "error": 404,
  "message": "Not Found",
  "success": false
}
```

##### POST '/quizzes'
```
 - Fetches a question to play quiz
 - Request Body: 
    - previous_questions constains a list of ids for previously attempted questions
    - quiz_category contains the id of the question category for the quiz
    {
        "previous_questions": [],
        "quiz_category": {  "id": "1"}
    }
- returns question to play quiz
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}

```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```