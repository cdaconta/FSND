import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#this function will paginate the result questions to 10 per page
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
  
  #This sets up CORS to Allow '*' for origins. 
  CORS(app)
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
   
  #This endpoint handles GET requests for categories
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()

    # 404 if no categories found
    if (len(categories) == 0):
        abort(404) 
    
    data = {}  

    for item in categories:
        data[item.id] = item.type
            
    return jsonify({
        'success':True,
        'categories': data
    })

  '''
  This endpoint handles GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint returns a list of questions, 
  number of total questions, current category, categories.
  '''
  @app.route('/questions')
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    # 404 if there are no questions
    if (len(questions) == 0):
            abort(404)

    questions_paginated = paginate(request, questions)
    categories = Category.query.order_by(Category.type).all()
    
    # 404 if there are no questions_paginated
    if (len(questions_paginated) == 0):
            abort(404)

    category_data = {}

    for item in categories:
      category_data[item.id] = item.type
        
    return jsonify({
      'success': True,
      'questions': questions_paginated,
      'total_questions': len(questions),
      'categories': category_data,
      'current_category':None

    })

  #This endpoint is used to DELETE question using a question ID.  
  @app.route("/questions/<int:question_id>", methods=['DELETE'])
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
            abort(404)
        finally:
            question.close()


  #This endpoint is used to POST a new question.
  @app.route('/questions', methods=['POST'])
  def create_questions():
    data = request.get_json()

    new_question = data.get('question')
    new_answer = data.get('answer')
    new_difficulty = data.get('difficulty')
    new_category = data.get('category')

    #Error if new_question or new_answer is None
    if ((new_question is None) or (new_answer is None)
        or (new_difficulty is None) or (new_category is None)):
        abort(422)

    try:
      question_obj = Question(
      question = new_question,
      answer = new_answer,
      difficulty = new_difficulty,
      category = new_category  

      )

      question_obj.insert()
      return jsonify({
                'success': True,
                'created': question_obj.id  
            })
    except:
      question_obj.rollback()
      abort(422)
    finally:
      question_obj.close()

  '''
  This POST endpoint is used to get questions based on a search term. 
  It will return any questions for whom the search term 
  is a substring of the question. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    try:
      data = request.get_json()
      search_box = data.get('searchTerm')

      #Error if search is submitted empty or is None
      if(search_box == '' or search_box is None):
        abort(404)

      # query to get result that is 'like' what is searched for 
      search_data = Question.query.filter(Question.question.ilike(f'%{search_box}%')).all()

      return jsonify(
        {
      "success":True,
      "questions": [question.format() for question in search_data],
      "total_questions": len(search_data),
      "current_category":None
        }
      )
    except:
      abort(404)

  '''
  This GET endpoint is used to get questions based on category. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):

      questions = Question.query.filter(Question.category==category_id).all()
      #Error if no questions exist
      if len(questions) == 0:
        abort(404)

      questions_paginated = paginate(request, questions)

      return jsonify({
        'success':True,
        'questions': questions_paginated,
        'total_questions': len(questions),
        'current_category': category_id
      })

  '''
  This POST endpoint is used to get questions to play the quiz. 
  This endpoint will take the category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  def get_question_quiz():
    data = request.get_json()

    previousQuestions = data.get('previous_questions')
    quizCategory = data.get('quiz_category')
   
    # abort 400 if quizCategory or previousQuestions is None
    if ((quizCategory is None) or (previousQuestions is None)):
          abort(400)
    
    if quizCategory['type'] == 'click':
        filtered_result = Question.query.filter(Question.id.notin_(previousQuestions)).all()
    else:
        filtered_result = Question.query.filter(Question.category==quizCategory['id'], Question.id.notin_(previousQuestions)).all()
    
    num = random.randint(0, len(filtered_result) - 1)

    random_question = filtered_result[num].format()
    
    return jsonify({
        'success': True,
        'question': random_question
    })
    
  '''
  These are error handlers for all expected errors 
  including 400, 404, and 422. 
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

    