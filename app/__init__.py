from flask import Flask
from config import Config
#__name__ is a python predefined variable that is passed to the name of the module in which it is used

app = Flask(__name__)
app.config.from_object(Config)

#passing __name__ will configure Flask the correct way
from app import routes  #route is imported at the bottom to avoid circular imports
