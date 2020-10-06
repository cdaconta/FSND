from myENV import *
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

user = os.environ.get('USER')
password = os.environ.get('PASSWORD')

class UnitTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_unit_test"
        self.database_path = "postgres://{}/{}".format(f'{user}:{password}@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

       # example question for use in tests
        self.new_question = {
            'question': 'What species are modern human beings?',
            'answer': 'Homo Sapiens',
            'difficulty': 2,
            'category': 1
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


    def test_pagination(self):
        """Test pagination failure 404"""
    
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        #check the response 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        
    def test_404_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
#----------------------------------------------------------------start here---------
    def test_get_categories(self):
        """Tests Get Categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_non_existing_category_404(self):
        """Test Non-Existing Category 404"""
        res = self.client().get('/categories/87')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete(self):
        """Tests question delete"""

        # create a new question to be deleted
        question = Question(question=self.new_question['question'], 
                            answer=self.new_question['answer'],
                            category=self.new_question['category'], 
                            difficulty=self.new_question['difficulty']
                            )
        question.insert()

        question_id = question.id

        # get number of questions before delete operation
        number_of_questions_initially = len(Question.query.all())

        # delete the question and store response
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        # get number of questions after the delete
        number_of_questions_after_delete = len(Question.query.all())

        # check if the question has been deleted
        question = Question.query.filter(Question.id == question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertTrue(len(number_of_questions_initially) - len(number_of_questions_after_delete) == 1)
        self.assertEqual(question, None)
#-------------------------------------------------check http 422
    def test_deleting_non_existing_question_422(self):
      res = self.client().delete('/question/999999')
      data = res.loads(res.data)

      self.assertEqual(res.status_code, 422)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'unprocessable')
#------------------------------------------------------------here
    def test_add_a_question(self):
        # create a new question to be deleted
        question = Question(question=self.new_question['question'], 
                            answer=self.new_question['answer'],
                            category=self.new_question['category'], 
                            difficulty=self.new_question['difficulty']
                            )
        total_questions_initially = len(Question.query.all())
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)
        total_questions_after_adding = len(Question.query.all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(total_questions_after_adding, total_questions_initially + 1)

    def test_add_question_422(self):
        question = {
            'question': 0
        }
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_search_questions(self):
        search = {'searchTerm': 'E'}
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_search_question_404(self):
        search = {
            'searchTerm': '~',
        }
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_get_questions_by_category_404(self):
        res = self.client().get('/categories/999999/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_play_quiz(self):
        quiz = {'previous_questions': [],
                          'quiz_category': {'type': 'Science', 'id': 1}}

        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz_404(self):
        quiz = {'previous_questions': []}
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")



# Make the tests executable
if __name__ == "__main__":
    unittest.main()