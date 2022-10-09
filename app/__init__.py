from datetime import datetime
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth




app = Flask(__name__)
CORS(app)
app.config.from_object(Config)


basic_auth = HTTPBasicAuth
token_auth = HTTPTokenAuth
 


db = SQLAlchemy(app)
migrate = Migrate(app,db)

