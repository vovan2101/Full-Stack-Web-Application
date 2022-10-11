from . import bp as auth
from flask import jsonify, request, flash
from .models import User
from .http_auth import basic_auth, token_auth



@auth.route('/users', methods = ['POST', 'GET'])
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


@auth.route('/token', methods = ['POST', 'GET'])
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token})
  

@auth.route('/users/<int:id>', methods = ["PUT"])
@token_auth.login_required
def update_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to update this user'}), 403
    user =  User.query.get_or_404(id)
    data = request.json
    user.update(data)
    return jsonify(user.to_dict())


@auth.route('/users/<int:id>', methods = ['DELETE'])
@token_auth.login_required
def delete_user(id):
    current_user = token_auth.current_user()
    if current_user.id != id:
        return jsonify({'error': 'You do not have access to delete this user'}), 403
    user_to_delete = User.query.get_or_404(id)
    user_to_delete.delete()
    return jsonify({'success': f'{user_to_delete.username} has been deleted'})


@auth.route('/me')
@token_auth.login_required
def me():
    return token_auth.current_user().to_dict()
