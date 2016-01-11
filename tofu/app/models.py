from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(1024))
    star = db.Column(db.Float)
    image_url = db.Column(db.String(256))
    movietags = db.relationship('MovieTag',backref='movies',lazy='dynamic')
    moviecollects = db.relationship('MovieCollect',backref='collector',lazy='dynamic')
    comments = db.relationship('Comment',backref='movies',lazy='dynamic')

class MovieTag(db.Model):
    __tablename__ = 'movietags'
    id = db.Column(db.Integer,primary_key=True)
    movie_id = db.Column(db.String(64), db.ForeignKey('movies.movie_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(256))
    movietags = db.relationship('MovieTag',backref='tags',lazy='dynamic')

class MovieCollect(db.Model):
    __tablename__='moviecollect'
    id = db.Column(db.Integer,primary_key=True)
    movie_id = db.Column(db.Integer,db.ForeignKey('movies.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    moviecollects = db.relationship('MovieCollect',backref='collects',lazy='dynamic')
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
