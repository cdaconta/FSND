#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import logging
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

#connects to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = "venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String()))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))  
    phone = db.Column(db.String(120))
    website = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='venue', lazy='select', cascade='all, delete-orphan')

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': [],
            'upcoming_shows': [],
            'past_shows_count': 0,
            'upcoming_shows_count': 0
        }

    def __repr__(self):
        return '<Venue {}>'.format(self.name)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = "artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    genres = db.Column(db.ARRAY(db.String(120)))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='artist', lazy='select', cascade='all, delete-orphan')

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'image_link': self.image_link,
            'past_shows': [],
            'upcoming_shows': [],
            'past_shows_count': 0,
            'upcoming_shows_count': 0
        }
    
    def __repr__(self):
        return '<Artist {}>'.format(self.name)


class Shows(db.Model):
  __tablename__ = "shows"

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  start_time = db.Column(db.DateTime)

  def __repr__(self):
        return '<Shows {}>'.format(self.artist_id, self.venue_id)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
# use a string for the value arg when calling this function
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  Data = []
  #this is like a select * from venue;
  all_venue = Venue.query.all()
  # Query to group by state and city
  venue_state_list = Venue.query.with_entities(Venue.state, Venue.city).group_by(Venue.state, Venue.city).order_by(Venue.state).all()

  for item in venue_state_list:
    Data.append({
      "city": item[1],
      "state": item[0], 
      "venues": [],
    })
  
  for venue in all_venue:
         
    upcoming_count = 0
    todays_date = datetime.now()
    #get all shows from each venue
    shows = Shows.query.filter_by(venue_id=venue.id).all()

    for item in shows:
      if item.start_time > todays_date:
        upcoming_count += 1
   
    for location in Data:
      if venue.state == location['state'] and venue.city == location['city']:
        location['venues'].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": upcoming_count
        })
        
  return render_template('pages/venues.html', areas=Data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_box = request.form.get('search_term', '')
  # query to get result that is 'like' what is searched for 
  search_data = Venue.query.filter(Venue.name.ilike(f'%{search_box}%'))
  
  response={
    "count": search_data.count(),
    "data": search_data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_box)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  #here i use class method details to return this particular venue details
  data = Venue.details(venue)

#query to get all past show that match this venue
  past_shows = db.session.query(Artist, Shows).join(Shows).join(Venue).\
    filter(
        Shows.venue_id == venue_id,
        Shows.artist_id == Artist.id,
        Shows.start_time < datetime.now()
    ).\
    all()
  #query to get all future show that match this venue
  upcoming_shows = db.session.query(Artist, Shows).join(Shows).join(Venue).\
    filter(
        Shows.venue_id == venue_id,
        Shows.artist_id == Artist.id,
        Shows.start_time > datetime.now()
    ).\
    all()

  for artist, show in past_shows:
        data['past_shows'].append({
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%Y-%m-%d, %H:%M")
        })
  for artist, show in upcoming_shows:
        data['upcoming_shows'].append({
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%Y-%m-%d, %H:%M")
        })
  data['upcoming_shows_count'] = len(upcoming_shows)
  data['past_shows_count'] = len(past_shows)
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    # get form data and create 
    form = VenueForm()
    form_venue = Venue(
      name = form.name.data, 
      genres = form.genres.data,
      address = form.address.data,
      city = form.city.data, 
      state = form.state.data,  
      phone = form.phone.data, 
      website = form.website.data, 
      facebook_link = form.facebook_link.data,
      seeking_talent = form.seeking_talent.data,
      seeking_description = form.seeking_description.data,
      image_link = form.image_link.data
       )
    
    # commit session to database
    db.session.add(form_venue)
    db.session.commit()
    # flash success 
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    #flash failure
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue_id)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artist_list = Artist.query.with_entities(Artist.id, Artist.name)

  Data = []

  for item in artist_list:
    Data.append({
        "id": item.id,
        "name": item.name
    })

  return render_template('pages/artists.html', artists=Data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_box = request.form.get('search_term', '')
  #query to get result 'like' what is typed in search box
  search_data = Artist.query.filter(Artist.name.ilike(f'%{search_box}%'))
  
  response={
    "count": search_data.count(),
    "data": search_data
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_box)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)

  data = Artist.details(artist)
  
  #query to get all past shows that match this artist
  past_shows = db.session.query(Venue, Shows).join(Shows).join(Artist).\
    filter(
        Shows.venue_id == Venue.id,
        Shows.artist_id == artist_id,
        Shows.start_time < datetime.now()
    ).\
    all()
    #query to get all future shows that match this artist
  upcoming_shows = db.session.query(Venue, Shows).join(Shows).join(Artist).\
    filter(
        Shows.venue_id == Venue.id,
        Shows.artist_id == artist_id,
        Shows.start_time > datetime.now()
    ).\
    all()

  for venue, show in past_shows:
        data['past_shows'].append({
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time.strftime("%Y-%m-%d, %H:%M")
        })
  for venue, show in upcoming_shows:
        data['upcoming_shows'].append({
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time.strftime("%Y-%m-%d, %H:%M")
        })
  data['upcoming_shows_count'] = len(upcoming_shows)
  data['past_shows_count'] = len(past_shows)

  return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  band = Artist.query.get(artist_id)
  #use class method details to get this artist details
  artist = Artist.details(band)
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    
    artist.name = form.name.data
    artist.genres = form.genres.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data 
    artist.website = form.website.data
    artist.facebook_link = form.facebook_link.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    artist.image_link = form.image_link.data

    db.session.commit()
    flash('The Artist ' + request.form['name'] + ' has been successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  spot = Venue.query.get(venue_id)
  #use class method to get this venues details
  venue = Venue.details(spot)
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    
    venue.name = form.name.data
    venue.genres = form.genres.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.phone = form.phone.data 
    venue.website = form.website.data
    venue.facebook_link = form.facebook_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    venue.image_link = form.image_link.data

    db.session.commit()
    flash('The Venue ' + request.form['name'] + ' has been successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    form = ArtistForm()
    
    form_artist = Artist(
    name = form.name.data,
    genres = form.genres.data,
    city = form.city.data,
    state = form.state.data,
    phone = form.phone.data,
    website = form.website.data,
    facebook_link = form.facebook_link.data,
    seeking_venue = form.seeking_venue.data,
    seeking_description = form.seeking_description.data,
    image_link = form.image_link.data,
    )

    db.session.add(form_artist)
    db.session.commit()
    flash('The Artist ' + request.form['name'] + ' has been successfully updated!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Shows.query.all()
  data = []

  for item in shows:
    data.append({
      'venue_id': item.venue_id,
      'venue_name':item.venue.name,
      'artist_id': item.artist_id,
      'artist_name':item.artist.name,
      'artist_image_link':item.artist.image_link,
      'start_time': format_datetime(str(item.start_time))
    })
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    form = ShowForm()
    
    form_show = Shows(
    artist_id = form.artist_id.data,
    venue_id = form.venue_id.data,
    start_time = form.start_time.data  
    )

    db.session.add(form_show)
    db.session.commit()
    flash('Success! Show could be listed.')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
