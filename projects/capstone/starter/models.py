# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

# ---------------------------------------------------------
# App Config.
# ---------------------------------------------------------

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "ufcfan"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()
moment = Moment()


# Set-up database-related Flask modules.
def setup_db(app, database_path=database_path):
    app.config.from_pyfile('config.py', silent=False)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    moment.app = app
    db.init_app(app)
    db.create_all()

# ---------------------------------------------------------
# Models.
# ---------------------------------------------------------


# Creating the debatase for Actors
class Fighter(db.Model):
    __tablename__ = 'fighters'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    arm_reach = db.Column(db.String)
    leg_reach = db.Column(db.String)
    sex = db.Column(db.String(1))
    win = db.Column(db.Integer)
    loss = db.Column(db.Integer)
    draw = db.Column(db.Integer)
    division = db.Column(db.Integer)

    def __repr__(self):
        return f"<Fighter id='{self.id}' first_name='{self.first_name}' last_name='{self.last_name}' age='{self.age}'\
            height='{self.height}' weight='{self.weight}' arm_reach='{self.arm_reach}' leg_reach='{self.leg_reach}' sex='{self.sex}' \
                win='{self.win}' loss='{self.loss}' draw='{self.draw}' division = '{self.division}'>"

    def __init__(self, first_name, last_name, age, height, weight, arm_reach, leg_reach, sex, win, loss, draw, division):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.height = height
        self.weight = weight
        self.arm_reach = arm_reach
        self.leg_reach = leg_reach
        self.sex = sex
        self.win = win
        self.loss = loss
        self.draw = draw
        self.division = division
        

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'age':self.age,
            'height':self.height,
            'weight':self.weight,
            'arm_reach':self.arm_reach,
            'leg_reach':self.leg_reach,
            'sex':self.sex,
            'win':self.win,
            'loss':self.loss,
            'draw':self.draw,
            'division':self.division,
        }

class Division(db.Model):
    __tablename__ = 'divisions'

    id = db.Column(db.Integer, primary_key=True)
    men_flyweight = db.Column(db.Integer)
    men_bantamweight = db.Column(db.Integer) 
    men_featherweight = db.Column(db.Integer)
    men_lightweight = db.Column(db.Integer)
    men_welterweight = db.Column(db.Integer)
    men_middleweight = db.Column(db.Integer)
    men_lightheavyweight = db.Column(db.Integer)
    men_heavyweight = db.Column(db.Integer)
    women_strawweight = db.Column(db.Integer)
    women_flyweight = db.Column(db.Integer)
    women_bantamweight = db.Column(db.Integer)
    women_featherweight = db.Column(db.Integer)

    def __init__(self, men_flyweight, men_bantamweight, men_featherweight, men_lightweight, men_welterweight, 
men_middleweight, men_lightheavyweight, men_heavyweight, women_strawweight, women_flyweight, women_bantamweight, women_featherweight):
        self.men_flyweight = men_flyweight
        self.men_bantamweight = men_bantamweight
        self.men_featherweight = men_featherweight
        self.men_lightweight = men_lightweight
        self.men_welterweight = men_welterweight
        self.men_middleweight = men_middleweight
        self.men_lightheavyweight = men_lightheavyweight
        self.men_heavyweight = men_heavyweight
        self.women_strawweight = women_strawweight
        self.women_flyweight = women_flyweight
        self.women_bantamweight = women_bantamweight
        self.women_featherweight = women_featherweight

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id':self.id,
            'men_flyweight':self.men_flyweight,
            'men_bantamweight':self.men_bantamweight,
            'men_featherweight':self.men_featherweight,
            'men_lightweight':self.men_lightweight,
            'men_welterweight':self.men_welterweight,
            'men_middleweight':self.men_middleweight,
            'men_lightheavyweight':self.men_lightheavyweight,
            'men_heavyweight':self.men_heavyweight,
            'women_strawweight':self.women_strawweight,
            'women_flyweight':self.women_flyweight,
            'women_bantamweight':self.women_bantamweight,
            'women_featherweight':self.women_featherweight,
        }
    