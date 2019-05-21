from flask import render_template
from app import app
from flask import render_template
from app.forms import LoginForm


@app.route('/') #@app.route decorator creates an association between the URL given as an argument and the function
@app.route('/index')
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
    return render_template('index.html', title='Home', user=user, posts=posts)
    #template rendering is the proces of converting a template into a complete html
    #render_template() function invokes the Jinja2 template engine that comes bundled with the Flask framework

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
#login=login - is passing d form obj created to the template with d name form
