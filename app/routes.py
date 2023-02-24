from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm
from app.forms import RegistrationForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from datetime import datetime
from app.forms import EditProfileForm
import random

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'thomas'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='home', posts=posts)

@app.route('/contact')
def contact():
    return "My email is throse@packer.edu"

@app.route('/cool_poem')
def cool_poem():
    return '''
<html>
    <head
        <title>Here is a cool poem</title>
    </head>
    <body>
    "The red tiger is in its cage. yes Yes. the tiger is out."
    </body>
</html>'''

@app.route('/songs')
def songs():
    songs = [
        {'artist': {'creator':'the who'},
         'song': 'slip kid'
        },
        {'artist': {'creator':'kanye'},
         'song': 'flashing lights'
        },
        {'artist': {'creator':'charles griffes'},
         'song': 'the white peacock'
        }
    ]
    return render_template('songs.html', title='my_songs', songs=songs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/quotes')
def quotes():
    quote_storage = {
  "Motiv": ["You can do it!", "Just believe!", "Never stop!", "You are him.", "Never doubt yourself, ever.", "You are the best player in the game.", "Everybody is counting on you.", "In spite of everything you've done for them, eventually they will hate you.", "Those who doubted you will soon retell how they met you."],
  "Fun": ["He he ha ha", "Your mother", "Joe mama", "Throw it on a dime", "Do you want to get candy?", "I missed the rage!!!!", "Its genover", "stewie, its not your fault, its not your fault","two L's make a Y, get em up, take it down, amariLLO, LLamar, me LLamo"],
  "Love" : ["You are my sunshine.", "I'm so glad we are together.", "Always be by my side.", "All that you are is all I ever need.", "Every moment is a good one with you."],
        }
    random_quotes = random.choice(list(quote_storage.values()))
    x = random.choice(random_quotes)
    return render_template('quotes.html', title= 'quotes')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
