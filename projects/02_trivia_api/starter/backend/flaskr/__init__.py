import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, query_result):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [item.format() for item in query_result]
  results = questions[start:end]
  return results

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()

    #logging.error(f'This is categories -- {categories}')
    
    data = []

    # 404 if no categories found
    if (len(categories) == 0):
        abort(404) 

    for item in categories:
        data.append({
            'success':True,
            'categories':item.format()
            }
        )
    

    return jsonify(data)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.
  

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    questions_paginated = paginate(request, questions)
    categories = Category.query.order_by(Category.type).all()
    category_data = []

    #num = len(questions)

    for item in categories:
      category_data.append({
        'id':item.id,
        'type':item.type
      })

    return jsonify({
      'success': True,
      'questions': questions_paginated,
      'total_questions': len(questions),
      'categories': category_data,
      'current_category':None

    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            question.rollback()
            abort(422)
        finally:
            question.close()
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_questions():
    data = request.get_json()

    new_question = data.get('question', None)
    new_answer = data.get('answer', None)
    new_difficulty = data.get('difficulty', None)
    new_category = data.get('category', None)

    try:
    question_obj = Question(
      question = new_question,
      answer = new_answer,
      difficulty = new_difficulty,
      category = new_category  #may need ['id']

    )

    question_obj.insert()
    return jsonify({
                'success': True,
                'created': question_obj.id  #not sure if necessary
            })
    except:
      question_obj.rollback()
      abort(422)
    finally:
      question_obj.close()
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  """ success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      }, """
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
      search_box = request.form.get('search_term', '')
  # query to get result that is 'like' what is searched for 
      search_data = Question.query.filter(Question.question.ilike(f'%{search_box}%'))
  
      response={
      "success":True,
      "questions": search_data,
      "total_questions": len(search_data),
      "current_category":None

      }

      return jsonify(response)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
      category_name = Category.query.get(category_id)
      questions = Question.query.filter_by(Question.category = category_name).all()

      question_data = []

      for item in questions:
        data.append({
          item.format()
        })

      return jsonify({
        'success':True,
        'questions': question_data,
        'total_questions': len(questions),
        'current_category': category_id
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  def get_question_quiz():
    data = request.get_json()

    previousQuestion = data.get('previous_questions')
    quizCategory = data.get('quiz_category')

    # abort 400
      if ((quizCategory is None) or (previousCategory is None)):
          abort(400)

    # if ALL is selected
      if (quizCategory['id'] == 0):
            questions = Question.query.all()
        # questions for given category
      else:  #not sure if we need ['id']
            questions = Question.query.filter_by(category=quizCategory['id']).all()

#-----------------------------work needed
    
      if cid == 0:
        selection = Question.query.filter(Question.id.notin_(previousQuestion)).all()
      else:
        selection = Question.query.filter(Question.category==cid, Question.id.notin_(previousQuestion)).all()
    random.randint(1, 10)
    
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

  @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    
  return app

    