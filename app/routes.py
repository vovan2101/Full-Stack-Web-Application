from app import app,db
from flask import jsonify


@app.route('/', methods = ['GET'])
def get_articles():
    return jsonify({'Hello': 'World'})