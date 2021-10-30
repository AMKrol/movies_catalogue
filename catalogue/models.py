from . import db
import datetime


class FavMovies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieID = db.Column(db.Integer)
    username = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)