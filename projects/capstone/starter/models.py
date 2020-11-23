# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

# ---------------------------------------------------------
# App Config.
# ---------------------------------------------------------

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

#connects to a local postgresql database
migrate = Migrate(app, db)


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
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    arm_reach = db.Column(db.Float)
    leg_reach = db.Column(db.Float)
    sex = db.Column(db.String(1))
    win = db.Column(db.Integer)
    loss = db.Column(db.Integer)
    draw = db.Column(db.Integer)
    division = db.Column(db.Integer, db.ForeignKey('fighters.id'))
    rank = db.Column(db.Integer)
    events = db.relationship('Event', backref = 'fighter', lazy='select', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Fighter id='{self.id}' first_name='{self.first_name}' last_name='{self.last_name}' age='{self.age}'\
            height='{self.height}' weight='{self.weight}' arm_reach='{self.arm_reach}' leg_reach='{self.leg_reach}' sex='{self.sex}' \
                win='{self.win}' loss='{self.loss}' draw='{self.draw}' division = '{self.division}' rank='{self.rank}'>"

    def __init__(self, first_name, last_name, age, height, weight, arm_reach, leg_reach, sex, win, loss, draw, division, rank):
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
        self.rank = rank
        

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
            'rank':self.rank,
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
    fighters = db.relationship('Fighter', backref='division', lazy='select', cascade='all, delete-orphan')
    events = db.relationship('Event', backref = 'division', lazy='select', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Division id='{self.id}' men_flyweight='{self.men_flyweight}' men_bantamweight='{self.men_bantamweight}' men_featherweight='{self.men_featherweight}'\
            men_lightweight='{self.men_lightweight}' men_welterweight='{self.men_welterweight}' men_middleweight='{self.men_middleweight}' men_lightheavyweight='{self.men_lightheavyweight}' men_heavyweight='{self.men_heavyweight}' \
                women_strawweight='{self.women_strawweight}' women_flyweight='{self.women_flyweight}' women_bantamweight='{self.women_bantamweight}'  women_featherweight='{self.women_featherweight}' >"

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

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String)
    event_date = db.Column(db.DateTime) 
    location = db.Column(db.String)
    division = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    fighter_1 = db.Column(db.Integer, db.ForeignKey('fighters.id'))
    fighter_2 = db.Column(db.Integer, db.ForeignKey('fighters.id'))
    fighter_1_votes = db.Column(db.Integer, default = 0)
    fighter_2_votes = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f"<Event id='{self.id}' event_name='{self.event_name}' event_date='{self.event_date}' location='{self.location}'\
            division='{self.division}' weight='{self.weight}' fighter_1='{self.fighter_1}' fighter_2='{self.fighter_2}' fighter_1_votes='{self.fighter_1_votes}' \
                fighter_2_votes='{self.fighter_2_votes}' >"

    def __init__(self, event_name, event_date, location, division, fighter_1, fighter_2, fighter_1_votes, fighter_2_votes) -> None:
        self.event_name = event_name
        self.event_date = event_date
        self.location = location
        self.division = division
        self.fighter_1 = fighter_1
        self.fighter_2 = fighter_2
        self.fighter_1_votes = fighter_1_votes
        self.fighter_2_votes = fighter_2_votes

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'event_name':self.event_name, 
            'event_date':self.event_date, 
            'division':self.division,
            'fighter_1':self.fighter_1,
            'fighter_2':self.fighter_2,
            'fighter_1_votes':self.fighter_1_votes,
            'fighter_2_votes':self.fighter_2_votes,
        }