# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

The Coffee Shop project is a full stack drink menu application. The application presents the user with:

1) Displays graphics representing the ratios of ingredients in each drink.
2) Allows public users to view drink names and graphics.
3) Allows the shop baristas to see the recipe information.
4) Allows the shop managers to create new drinks and edit existing drinks.

## How to setup

Start by reading the READMEs in:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## About the Stack

These are the key functional areas:

### Backend

The `./backend` directory contains a Flask server with an SQLAlchemy module.  There are Flask endpoints that are configured to integrate with Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
