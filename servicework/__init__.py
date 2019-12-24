"""
__init__.py file is responsible for:

1) Creating an instance of flask. 
2) Creating and connecting to SQLAlchemy database. 
3) Enabling hashing for user authentication.
4) Enabling LoginManager to handle user login verificatoin details. 
5) Brings in our routes for connectivity. 

Links ara available for module documentation. 
"""

from flask import Flask                                         # https://flask.palletsprojects.com/en/1.1.x/quickstart/
from flask_sqlalchemy import SQLAlchemy                         # https://flask-sqlalchemy.palletsprojects.com/en/2.x/
from flask_bcrypt import Bcrypt                                 # https://flask-bcrypt.readthedocs.io/en/latest/
from flask_login import LoginManager                            # https://flask-login.readthedocs.io/en/latest/

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'   
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'    
db = SQLAlchemy(app)                                            
bcrypt = Bcrypt(app)                                            
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from servicework import routes