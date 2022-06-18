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
migrate = Migrate (app, db)

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
    facebook_link = db.Column(db.String(120))
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
    website_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String())
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
   #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
#

    return render_template('pages/venues.html', 
    areas=Venue.query.all()
    )

 
 

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  search_term = request.form.get('search_term', '')
  
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

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


@app.route('/venues/delete/<venue_id>')
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
  search_term = request.form.get('search_term', '')
 
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

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

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist_to_edit)

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
  return redirect(url_for('show_artist'), artist_id=artist_id)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_to_edit = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue_to_edit)
  
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
  
  return render_template('pages/shows.html', 
  shows=Show.query.all()
  # venues=Venue.query.all(),
  # artists= Artist.query.all()
  )
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

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
