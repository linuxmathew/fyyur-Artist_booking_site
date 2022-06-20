#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import sys
from operator import ge
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import false
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate (app, db, compare_type=True)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    seeking_talent=db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    website_link=db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String()))
    upcoming_shows = db.relationship('Show', backref="venue", lazy=True)
  

    # TODO: implement any missing fields, as a database migration using Flask-Migrate [DONE]

class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    seeking_description = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    upcoming_shows = db.relationship('Show', backref="artist", lazy=True)
    
 

    # TODO: implement any missing fields, as a database migration using Flask-Migrate [DONE]
    
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. [DONE]
# This Implement Many to Many relationship between the Artist and the Venue.
## ...as it is possible for many artists to perform shows in many Venues
class Show(db.Model):
  __tablename__ = 'show'
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data. [DONE]
  #let's create an empty array for our datas
  data_values = []
  
  # let's query the database for all values in venue Model
  venues = Venue.query.all()

  # let's use set to avoid duplicate in venues
  our_locations = set()

  for all_value in venues:
      # add city/state tuples
    our_locations.add((all_value.city, all_value.state))

  # for each distinct state and city, let's add venues
  for location in our_locations:
    data_values.append({
        "city": location[0],
        "state": location[1],
        "venues": []
    })

  for venue in venues:
    num_upcoming_shows = 0

    our_shows = Show.query.filter_by(venue_id=venue.id).all()

    # get current date to filter num_upcoming_shows
    current_date = datetime.now()

    for show in our_shows:
      if show.start_time > current_date:
          num_upcoming_shows += 1

    for the_venue_location in data_values:
      if venue.state == the_venue_location['state'] and venue.city == the_venue_location['city']:
        the_venue_location['venues'].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": num_upcoming_shows
        })
  return render_template('pages/venues.html', areas=data_values)
   #      num_upcoming_shows should be aggregated based on number of upcoming shows per venue.


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  search_input = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike(f'%{search_input}%'))

  search_output={
    "count": result.count(),
    "data": result
  }
  
  
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  return render_template('pages/search_venues.html', results=search_output, search_term=search_input)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  
  # TODO: replace with real venue data from the venues table, using venue_id
  
  
  return render_template('pages/show_venue.html', 
  venue = Venue.query.get(venue_id)
  )

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  # TODO: insert form data as a new Venue record in the db, instead [DONE]
  #  TODO: modify data to be the data object returned from db insertion [DONE]
  try:
    name=request.form.get('name')
    city=request.form.get('city')
    state=request.form.get('state')
    address=request.form.get('address')
    phone=request.form.get('phone')
    genres=request.form.getlist('genres')
    facebook_link=request.form.get('facebook_link')
    image_link=request.form.get('image_link')
    website_link=request.form.get('website_link')
    seeking_talent= True if 'seeking_venue' in request.form else False
    seeking_description=request.form.get('seeking_description')

    new_venue = Venue(name=name, city=city, state=state, address=address, phone=phone, facebook_link=facebook_link,
    image_link=image_link, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description, genres=genres)
    db.session.add(new_venue)
    db.session.commit()

  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())

  finally:
    db.session.close()
# TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  if error: 
      flash('An error occurred. Venue ' + request.form['name']+ ' could not be listed.')
  # on successful db insert, flash success
  if not error: 
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')  


@app.route('/venues/<venue_id>/delete')
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    
    venue_to_delete = Venue.query.get(venue_id)
    db.session.delete(venue_to_delete)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue {venue.name} could not be deleted.')
  
  if not error:
    flash('Venue {venue.name} was successfully deleted.')
  return render_template('pages/home.html')
  

  # [DONE]BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  # TODO: replace with real data returned from querying the database
#  data=[{
#    "id": 4,
#    "name": "Guns N Petals",
#  }, {
#    "id": 5,
#    "name": "Matt Quevedo",
#  }, {
#    "id": 6,
#    "name": "The Wild Sax Band",
#  }]
  return render_template('pages/artists.html', artists=Artist.query.all()
  )

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_input = request.form.get('search_term', '')
 
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  result = Artist.query.filter(Artist.name.ilike(f'%{search_input}%'))

  search_output={
    "count": result.count(),
    "data": result
  }
  return render_template('pages/search_artists.html', results=search_output, search_term=search_input)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  return render_template('pages/show_artist.html', 
  artist = Artist.query.get(artist_id))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_to_edit = Artist.query.get(artist_id)
  values={
    "id": artist_to_edit.id,
    "name": artist_to_edit.name,
    "genres": artist_to_edit.genres,
    "state": artist_to_edit.state,
    "city": artist_to_edit.city,
    "phone": artist_to_edit.phone,
    "website_link": artist_to_edit.website_link,
    "image_link": artist_to_edit.image_link,
    "facebook_link": artist_to_edit.facebook_link,
    "seeking_venue": artist_to_edit.seeking_venue,
    "seeking_description":artist_to_edit.seeking_description
  }

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=values)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  artist_to_edit = Artist.query.get(artist_id)

  try:
    artist_to_edit.name = request.form.get('name')
    artist_to_edit.city = request.form.get('city')
    artist_to_edit.state = request.form.get('state')
    artist_to_edit.phone = request.form.get('phone')
    artist_to_edit.genres = request.form.getlist('genres')
    artist_to_edit.facebook_link = request.form.get('facebook_link')
    artist_to_edit.image_link = request.form.get('image_link')
    artist_to_edit.website_link = request.form.get('website_link')
    artist_to_edit.seeking_talent = True if 'seeking_venue' in request.form else False
    artist_to_edit.seeking_description = request.form.get('seeking_description')
  
    db.session.commit()
  
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())

  finally:
    db.session.close()

  if error:
    flash('An error occured. Artist could not be changed.')
  if not error:
    flash('Artist was successfully updated')
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_artist', artist_id=artist_id) )

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_to_edit = Venue.query.get(venue_id)
  values={
    "id": venue_to_edit.id,
    "name": venue_to_edit.name,
    "genres": venue_to_edit.genres,
    "state": venue_to_edit.state,
    "address": venue_to_edit.address,
    "city": venue_to_edit.city,
    "phone": venue_to_edit.phone,
    "website_link": venue_to_edit.website_link,
    "image_link": venue_to_edit.image_link,
    "facebook_link": venue_to_edit.facebook_link,
    "seeking_venue": venue_to_edit.seeking_venue,
    "seeking_description":venue_to_edit.seeking_description
  }
  return render_template('forms/edit_venue.html', form=form, venue=values)
  
  # TODO: populate form with values from venue with ID <venue_id>
  

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  venue_to_edit = Venue.query.get(venue_id)

  try:
    venue_to_edit.name = request.form.get('name')
    venue_to_edit.city = request.form.get('city')
    venue_to_edit.state = request.form.get('state')
    venue_to_edit.address = request.form.get('address')
    venue_to_edit.phone = request.form.get('phone')
    venue_to_edit.genres = request.form.getlist('genres')
    venue_to_edit.facebook_link = request.form.get('facebook_link')
    venue_to_edit.image_link = request.form.get('image_link')
    venue_to_edit.website_link = request.form.get('website_link')
    venue_to_edit.seeking_talent = True if 'seeking_talent' in request.form else False
    venue_to_edit.seeking_description = request.form.get('seeking_description')
    
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()

  if error:
    flash('An error occured. Venue could not be changed.')
  if not error:
    flash('Venue was successfully updated')
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False 
  
  try:
    name=request.form.get('name')
    city=request.form.get('city')
    state=request.form.get('state')
    phone=request.form.get('phone')
    genres=request.form.getlist('genres')
    facebook_link=request.form.get('facebook_link')
    image_link=request.form.get('image_link')
    seeking_venue= True if 'seeking_venue' in request.form else False
    seeking_description=request.form.get('seeking_description')
    website_link=request.form.get('website_link')
  # called upon submitting the new artist listing form
    
    new_artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link,
    seeking_description=seeking_description, seeking_venue=seeking_venue, website_link=website_link)
  # TODO: insert form data as a new Venue record in the db, instead
    db.session.add(new_artist)
    db.session.commit()  
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
    
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())

  finally:
    db.session.close()
  # TODO: on unsuccessful db insert, flash an error instead.

  if error:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')   
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.order_by(db.desc(Show.start_time))
  #let's make an empty array to store our value
  data_values=[]
  
  # displays list of shows at /shows
  for show in shows:
    data_values.append({
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist_id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time": format_datetime(str(show.start_time))
    })
  # TODO: replace with real venues data.
 
  return render_template('pages/shows.html', shows=data_values)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')

  new_show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
  db.session.add(new_show)
  db.session.commit()
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
