from app import app, db
from app.models import User, Post

@app.shell_context_processor    #registers the fxn below as a shell context function
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post} #we use a diction. bcos for each item we have to provide a name with which it will be referenced in the shell