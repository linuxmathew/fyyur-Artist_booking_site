#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment


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