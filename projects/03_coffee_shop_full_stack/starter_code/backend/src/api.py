import os
import re
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES

# Returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
@app.route('/drinks')
def get_drinks():
    try:
        all_drinks = Drink.query.all()
       
        return jsonify({
            'success':True,
            'drinks': [drink.short() for drink in all_drinks]
        }), 200
    except BaseException as e:
        print(e)
        abort(404)


# Returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
    try:
        all_drinks = Drink.query.all()
      
        return jsonify({
            'success':True,
            'drinks': [drink.long() for drink in all_drinks]
        }), 200
    except BaseException as e:
        print(e)
        abort(404)


# Returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
@app.route('/drinks', methods = ['POST'])
@requires_auth('post:drinks')
def create_drink(token):
    
    data = request.get_json()
    drink_title = data.get('title')
    drink_recipe = data.get('recipe')

    drink_obj = Drink(
            title = drink_title,
            recipe = json.dumps(drink_recipe)
            #recipe = drink_recipe
        )
    try:
        drink_obj.insert()
        
        return jsonify({
                'success':True,
                'drinks': [drink_obj.long()],
            }), 200

    except BaseException as e:
        print(e)
        drink_obj.rollback()
        abort(422)
    finally:
        drink_obj.close_session()

    
# Returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
@app.route('/drinks/<int:id>', methods = ['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(token, id):
    
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
            abort(404)

    drink_details = drink.long()
    
    data = request.get_json()
    
    drink_title = data.get('title')
    drink_recipe = data.get('recipe')

    drink_details['title'] = drink_title
    drink_details['recipe'] = drink_recipe

    return jsonify({
                'success':True,
                'drinks': [drink_recipe],
            }), 200


# Returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
@app.route('/drinks/<int:id>', methods = ['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(token, id):
   
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)

    drink.delete()
    return jsonify({
                'success':True,
                'delete': id,
            }), 200

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


@app.errorhandler(AuthError)
def authentification_failed(AuthError):
    return jsonify({
        "success": False,
        "error": AuthError.status_code,
        "message": AuthError.error
                    }), 401