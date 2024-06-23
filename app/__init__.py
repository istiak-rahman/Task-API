from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config
# set Flask configs for initialization of database
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)                             
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

from .models import Task, User

with app.app_context():
    db.create_all()

from app import routes