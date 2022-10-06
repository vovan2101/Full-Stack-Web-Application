from crypt import methods
import json
from lib2to3.pgen2 import token
from locale import currency
from app import app,db, basic_auth, token_auth
from flask import jsonify, request, make_response, flash
from app.models import Articles, User, check_password_hash



@app.route('/users', methods = ['POST', 'GET'])
def create_user():
    data = request.json
    for field in ['username', 'email', 'password']:
        if field not in data:
            return jsonify({'error': f"You are missing the {field} field"}), 400

    username = data['username']
    email = data['email']

    user_exists = User.query.filter((User.username == username) | (User.email == email)).all()
    if user_exists:
        return jsonify({'error': f"User with username {username} or email {email} already exists"}), 400
    elif len(username) < 4:
        flash('Username must be greater than 3 characters.')
    else:   
        new_user = User(**data)
        return jsonify(new_user.to_dict())


@app.route('/token', methods = ['POST', 'GET'])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token})
  

@app.route('/users/<int:id>', methods = ["PUT"])
@token_auth.login_required
def update_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to update this user'}), 403
    user =  User.query.get_or_404(id)
    data = request.json
    user.update(data)
    return jsonify(user.to_dict())


@app.route('/users/<int:id>', methods = ['DELETE'])
@token_auth.login_required
def delete_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to delete this user'}), 403
    user_to_delete = User.query.get_or_404(id)
    user_to_delete.delete()
    return jsonify({'success': f'{user_to_delete.username} has been deleted'})


@app.route('/me')
@token_auth.login_required
def me():
    return token_auth.current_user().to_dict()


@app.route('/get', methods = ['GET'])
def get_articles():
    articles = Articles.query.all()
    return jsonify([a.to_dict() for a in articles])


@app.route('/get/<int:id>', methods = ['GET'])
def article_details(id):
    article = Articles.query.get_or_404(id)
    return jsonify(article.to_dict())


@app.route('/articles', methods = ['POST'])
@token_auth.login_required
def create_article():
    if not request.is_json:
        return jsonify({'error': 'Please send a body'}), 400
    data = request.json
    for field in ['title', 'body']:
        if field not in data:
            return jsonify({'error': f'You are missing the {field} field'}),400
    current_user = token_auth.current_user()
    data['user_id'] = current_user.id
    new_article = Articles(**data)
    return jsonify(new_article.to_dict()),201


@app.route('/articles/<int:id>', methods = ['PUT'])
@token_auth.login_required
def update_article(id):
    article = Articles.query.get_or_404(id)
    user = token_auth.current_user()
    if user.id != article.user_id:
        return jsonify({'error': 'You are not allowed to edit this article'}),403
    data = request.json
    article.update(data)
    return jsonify(article.to_dict())


@app.route('/articles/<int:id>', methods = ['DELETE'])
@token_auth.login_required
def delete_article(id):
    article = Articles.query.get_or_404(id)
    user = token_auth.current_user()
    if user.id != article.user_id:
        return jsonify({'error': 'You are not allowed to delete this article'}),403
    article.delete()
    return jsonify({'success': f'{article.title} has been deleted'})