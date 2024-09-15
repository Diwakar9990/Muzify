from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Album, Song, Playlist
from app import app
from functools import wraps
import datetime

def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash('Login required')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner



# first route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# second route
@app.route('/login')
def login():
    return render_template('login.html')

# third route
@app.route('/register')
def register():
    return render_template('register.html')

# fourth route
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if username == '' or password == '':
        flash('Username or Password Cannot Be empty')
        return redirect(url_for('register'))
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Invalid username')
        return redirect(url_for('login'))   
    if not user.check_password(password):
        flash('Password is incorrect')
        return redirect(url_for('login'))
    else:
        session['user_id'] = user.id
        return redirect(url_for('home'))

# fifth route
@app.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' or password == '':
        flash('Username or Password Cannot Be empty')
        return redirect(url_for('register'))
    if User.query.filter_by(username=username).first():
        flash('User already registered please choose another username')
        return redirect(url_for('register'))
    user = User(username=username, password=password, name=name)
    db.session.add(user)
    db.session.commit()
    flash('user registrated successfully')
    return redirect(url_for('login'))

# sixth route

@app.route('/logout')
@auth_required
def logout():
    session.pop('user_id', None)
    flash('logout successful')
    return redirect(url_for('index'))


# seventh route

@app.route('/profile')
@auth_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

# eighth route

@app.route('/creator')
@auth_required
def creator():
    user = User.query.get(session['user_id'])
    user.is_creator = True
    db.session.commit()
    flash('Successfully registered as creator')
    return redirect(url_for('profile'))

# ninth route
@app.route('/home')
@auth_required
def home():
    query = request.args.get('query')
    if query:
        Songs = Song.query.filter(Song.name.like('%' + query + '%')).all()
    else:
        Songs= Song.query.all()
    user = User.query.get(session['user_id'])
   
    return render_template('home.html', user=user, song=Songs)

# tenth route
@app.route('/upload')
@auth_required
def upload():
    user = User.query.get(session['user_id'])
    return render_template('upload.html',
                            user=user,
                            nowstring=datetime.datetime.now().strftime('%y-%m-%d')
                            )

# eleventh route
@app.route('/upload', methods=['POST'])
@auth_required
def upload_post():
    user = User.query.get(session['user_id'])
    name = request.form.get('name')
    album = request.form.get('Album')
    lyrics = request.form.get('lyrics')
    date = datetime.datetime.now()
    file = request.form.get('file')
    artist = request.form.get('artist')
    genre = request.form.get('genre')

    song = Song(name=name, album=album, lyrics=lyrics, created_date=date, file=file, user_id=user.id)
    album = Album(name=album, artist=artist, genre=genre)
    db.session.add(song)
    db.session.add(album)
    db.session.commit()
    flash('Song uploaded successfully')
    return redirect(url_for('home'))

# twelvth route
@app.route('/showlyrics/<int:id>')
@auth_required
def showlyrics(id):
    song = Song.query.get(id)
    user = User.query.get(session['user_id'])
    return render_template('lyrics.html', user=user, song=song)

# thirteenth route

@app.route('/dashboard')
@auth_required
def dashboard():
   
    song = Song.query.all()
    user = User.query.get(session['user_id'])
    
    return render_template('dashboard.html', user=user, song=song)

# fourteenth route

@app.route('/dashboard/<int:id>/delete')
@auth_required
def delete(id):
    user = User.query.get(session.get('user_id'))
    Song.query.filter_by(id=id).delete()
    db.session.commit()
    if user.username == 'admin':
        return redirect(url_for('admin'))
    flash('Song deleted successfully')
    return redirect(url_for('dashboard'))

# fifteenth route

@app.route('/dashboard/<int:id>/update')
@auth_required
def update(id):
    song = Song.query.get(id)
    user = User.query.get(session['user_id'])
    return render_template('update.html', user=user, song=song)

# Sixteenth route

@app.route('/dashboard/<int:id>/update', methods=['POST'])
@auth_required
def update_now(id):
    song = Song.query.get(id)
    name = request.form.get('name')
    album = request.form.get('Album')
    lyrics = request.form.get('lyrics')
    song.name = name
    song.album = album 
    song.lyrics = lyrics
    db.session.commit()
    flash('Song details updated successfully')
    return redirect(url_for('dashboard'))

# Seventeenth route

@app.route('/admin')
@auth_required
def admin():
  
    user = User.query.all()
    user_count = User.query.count()
    creator_count = User.query.filter_by(is_creator=True).count()
    query = request.args.get('query')
    song_count = Song.query.count()
    if query:
        Songs = Song.query.filter(Song.name.like('%' + query + '%')).all()
    else:
        Songs= Song.query.all()
    return render_template('admin.html',
                           user=user, 
                           song=Songs, 
                           user_count=user_count,
                           creator_count=creator_count,
                           song_count=song_count)



