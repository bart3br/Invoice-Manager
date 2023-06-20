from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

#randomly generated 16 byte secret key (by running secrets.token_hex in terminal)
app.config['SECRET_KEY'] = 'cd427c1e4b942503f56b028cea251a64'

#database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from application import routes