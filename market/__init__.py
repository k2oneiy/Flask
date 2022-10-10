from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_manager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = "d597a71e21b5a9bffd3fbf99"  
app.debug = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from market import routes



