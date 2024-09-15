from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy(app)
from datetime import datetime
 
# models

@dataclass
class User(db.Model):

    id: int
    username: str
    passhash: str
    name: str
    is_admin: bool
    is_creator: bool

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passhash = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=True)
    is_creator = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    @property
    def password(self):
        raise AttributeError('You cannot read passwords')
    
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

@dataclass
class Song(db.Model):
    id: int
    name: str
    album: str
    lyrics: str
    created_date: str
    user_id : int
    file: str
    __tablename__ ='song'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    album = db.Column(db.String(80), nullable=False)
    lyrics = db.Column(db.String(512), nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file = db.Column(db.String(80), nullable=False)

    #relationship
    user = db.relationship('User', backref='songs', lazy=True)

class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), db.ForeignKey('song.album'))
    artist = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)

    # relationship
    songs = db.relationship('Song', backref='album_', lazy=True)


class Playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    
    # relationship
    songs = db.relationship('Song', backref='playlist_songs', lazy=True)
    user = db.relationship('User', backref='playlist_users', lazy=True)

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password='admin', is_admin=True)
        db.session.add(admin)
        db.session.commit()