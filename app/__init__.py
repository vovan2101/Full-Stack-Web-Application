from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.blueprints.auth import bp as auth
app.register_blueprint(auth)

from app.blueprints.blog import bp as blog
app.register_blueprint(blog)


