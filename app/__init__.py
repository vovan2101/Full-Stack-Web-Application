from datetime import datetime
from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .models import User
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)


basic_auth = HTTPBasicAuth
token_auth = HTTPTokenAuth


@basic_auth.verify_password
def verify(username, password):
    user = User.query.filter_by(username = username).first()
    if user and user.check_password(password):
        return user


@token_auth.verify_token
def verify(token):
    user = User.query.filter_by(token = token).first()
    if user and user.token_expiration > datetime.utcnow():
        return user  


db = SQLAlchemy(app)
migrate = Migrate(app,db)


from app import routes, models