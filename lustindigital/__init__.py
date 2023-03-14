from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '1749cad9d00ae746f00920a97d5f494b'
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lustin.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from lustindigital import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not engine.has_table('usuario'):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print('DB criado')
else:
    print('DB já existe no sistema')

from lustindigital import routes
