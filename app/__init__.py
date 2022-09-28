from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
ma = Marshmallow(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'You must be logged in to do that'


from . import routes, models