from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/') #@app.route decorator creates an association between the URL given as an argument and the function
@app.route('/index')
@login_required #a decorator to protect login() function from users that are not authenticated
def index():
    user = {'username':'Bolaji'}
    posts = [
        {
            'author': {'username':'Man'},
            'body' : 'Beautiful times are here!'
        },
        {
            'author': {'username': 'God'},
            'body': 'Good times have come!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)

#logging in users
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid user name or password!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

#There are actually three possible cases that need to be considered to determine where to redirect after a successful login:
#   If the login URL does not have a next argument:
#       then the user is redirected to the index page.
#
#    If the login URL includes a next argument that is set to a relative path (or in other words, a URL without the domain portion)
#       then the user is redirected to that URL.
#
#   If the login URL includes a next argument that is set to a full URL that includes a domain name:
#       then the user is redirected to the index page. This is to discourage an attacker from insering a URL leading to a malicious site

        if not next_page or url_parse(next_page).netloc != '':  #url_parse() determines whether the URL is relative or absoluts; and then check if netloc component is set or not
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

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

@app.route('/user/<username>')  #<> implies a dynamic component
@login_required
def user(username):
    #given the username, load the user from the database
    #if the username does not exist, the fxn will not return, and instead a 404 exception will be raised
    user = User.query.filter_by(username=username).first_or_404()
    #we create a fake list of posts for the returned(or unreturned) user
    posts = [
        {'author':user, 'body':'Test post #1'},
        {'author':user, 'body':'Test Post #2'}
    ]
    #we render a new 'user.html' template to which we pass the user object and the list of posts
    return render_template('user.html', user=user, posts=posts)

@app.before_request #registers the decorated fxn to be executed right before the view fxn below
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
#so we needn't add to session bcos when we reference current_user, Flask-Login will invoke the user
#loader callback fxn, which will run a database query that will put the target user in the database
#session. So it's not necessary to add the user again in this function
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
#if the above test returns true, i copy the data from the form into the user object and then write
#the object to the database. LOOK BELOW RETURN FOR MORE COMMENT

        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saves')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':

        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


'''validate_on_submit() could returns a False :
    A)bcos the browser sent a 'GET'(i.e form is being requested gor the first time) or
    B)bcos the browser sent a 'POST' request with some form data is invalid:
i)FOR CASE A: prepopulate the form with data that's stored in the db
we respond by providing an initial version of the form template. This is the reverse
of what we did during submission - move data stored in the user field to the form.
Those form fields will have the current data stored for the user.
ii)FOR CASE B: 'POST' is automatically checked for a submission with failed validation 
 we don't want to write anything on the form fields(which ia already populated by WTForms)
'''