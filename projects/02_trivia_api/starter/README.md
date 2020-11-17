This project is a _simple trivia game_.  On the landing page you are presented with basic navigation menus both horizontally and vertically, vertically are the categories to filter by as well as a search box to look for a particular question.  The horizontal menu consists of List, Add, and Play.  List triggers the landing page with the menus and all the questions in the database.  Add allows the user to submit a question, answer, a difficulty rating, as well as the category to the database.  Finally the Play tab in the menu goes to a quiz section that allow you to choose a category where a random question from that category will be presented.

# Getting Started

People using this project should already have Python, PIP, and Node.js which comes with NPM installed on their local machine.
*	https://www.python.org/
*	https://pypi.org/project/pip/
*	https://nodejs.org/en/

Clone the repository from github.com to your local machine.  

It is recommended to use a virtual environment for the project.  https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

Open two terminals to run the project. 
*	One for the backend and the other for the front end.

Navigate to the `/backend` directory and run in terminal:
```
	pip install -r requirements.txt
```

*	The key dependencies are Flask, SQLalchemy, and Flask-Cors.
*	To run the server, execute:
```
	export FLASK_APP=flaskr
	export FLASK_ENV=development
	flask run
```
* Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.
* Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.
*	On Windows 10 in the flaskr folder with PowerShell:
```
    $env:FLASK_APP = "__init__"
    $env:FLASK_DEBUG=1
    Flask run	
```
Next navigate to the `/frontend` directory and run:
```
Npm install
```
This will install all the necessary dependencies.

## Starting the Frontend

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 
Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.
```bash
npm start
```
## Testing

To run the tests, run
```
dropdb trivia_unit_test
createdb trivia_unit_test
psql trivia_unit_test < trivia.psql
```
Navigate to the `/backend` directory and run in terminal:
`python testUnit.py`

## API Reference

*	Base URL: Currently this application is only hosted locally. The backend is hosted at http://localhost:5000/
*	Authentication: This version does not require authentication or API keys.

## Error Handling

Errors are returned as JSON in the following format:
```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
The API will return three types of errors:
*	400 – bad request
*	404 – resource not found
*	422 – unprocessable

Endpoints (**All example curl commands will be difference in Powershell)

### GET /categories
*	General: Returns a list categories.
*	Example: curl http://localhost:5000/categories
```
  {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "success": true
  }
```
### GET /questions
*	General:
    *	Returns a list questions.
    *	Results are a paginated list of 10 questions.
    *	Also returns list of categories and total number of questions.

*	Example: curl http://localhost:5000/questions
```
  {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a      young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 28
}
```
### DELETE /questions/<int:id>
*	General:
    *	Deletes a question with a URL parameter.
    *	If successful it will return the id of deleted question.
	  * Example: curl http://localhost:5000/questions/1 -X DELETE
	    ```
        {
            "deleted": 1, 
            "success": true
        }
      ```
### POST /questions
*	General:
    *	Creates a new question using JSON parameters.
    *	Returns JSON object with “success” and the “created” id of item create.
    * Example: curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "What is the capital of New York State?", "answer": "Albany", "difficulty": 2, "category": "3" }'
      ```
        {
        "created": 50, 
        "success": true
        }
      ```
### POST /questions/search
* General:
    *	Searches for questions using search term in JSON parameters.
    *	Returns JSON object with matching questions paginated.
    * Example: curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "soccer"}'
      ```
        {
          "current_category": null, 
          "questions": [
            {
              "answer": "Brazil", 
              "category": 6, 
              "difficulty": 3, 
              "id": 10, 
              "question": "Which is the only team to play in every soccer World Cup tournament?"
            }, 
            {
              "answer": "Uruguay", 
              "category": 6, 
              "difficulty": 4, 
              "id": 11, 
              "question": "Which country won the first ever soccer World Cup in 1930?"
            }
          ], 
          "success": true, 
          "total_questions": 2
        }
  ```    
### GET /categories/<int:id>/questions
*	General:
    *	Gets questions by category id using URL parameters.
    *	Returns JSON object with matching questions paginated.
    * Example: curl http://localhost:5000/categories/1/questions
        ```
            {
              "current_category": "Science", 
              "questions": [
                  {
                      "answer": "The Liver", 
                      "category": 1, 
                      "difficulty": 4, 
                      "id": 20, 
                      "question": "What is the heaviest organ in the human body?"
                  }, 
                  {
                      "answer": "Alexander Fleming", 
                      "category": 1, 
                      "difficulty": 3, 
                      "id": 21, 
                      "question": "Who discovered penicillin?"
                  }, 
                  {
                      "answer": "Blood", 
                      "category": 1, 
                      "difficulty": 4, 
                      "id": 22, 
                      "question": "Hematology is a branch of medicine involving the study of what?"
                  }
              ], 
              "success": true, 
              "total_questions": 3
            }
        ``` 
### POST /quizzes
*	General:
    *	Uses JSON request parameters of the category and the previous questions.
    *	Returns JSON object with random question that is not a part of the previous questions.
    * Example: curl http://localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Art", "id": "2"}}'
        ```
          {
          "question": {
            "answer": "Jackson Pollock", 
            "category": 2, 
            "difficulty": 2, 
            "id": 19, 
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a  leading exponent of action painting?"
        }, 
          "success": true
        }
        ```
### Authors

Christian Daconta authored the __init__.py file and the unit test file called testUnit.py.
All the other project files were created by Udacity as a project template for the Full Stack Web Developer Nanodegree.
