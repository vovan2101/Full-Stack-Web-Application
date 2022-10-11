from . import bp as blog
from app.blueprints.auth.http_auth import token_auth
from flask import jsonify, request
from .models import Articles


@blog.route('/get', methods = ['GET'])
def get_articles():
    articles = Articles.query.all()
    return jsonify([a.to_dict() for a in articles])


@blog.route('/get/<int:id>', methods = ['GET'])
def article_details(id):
    article = Articles.query.get_or_404(id)
    return jsonify(article.to_dict())


@blog.route('/articles', methods = ['POST'])
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


@blog.route('/articles/<int:id>', methods = ['PUT'])
@token_auth.login_required
def update_article(id):
    article = Articles.query.get_or_404(id)
    user = token_auth.current_user()
    if user.id != article.user_id:
        return jsonify({'error': 'You are not allowed to edit this article'}),403
    data = request.json
    article.update(data)
    return jsonify(article.to_dict())


@blog.route('/articles/<int:id>', methods = ['DELETE'])
@token_auth.login_required
def delete_article(id):
    article = Articles.query.get_or_404(id)
    user = token_auth.current_user()
    if user.id != article.user_id:
        return jsonify({'error': 'You are not allowed to delete this article'}),403
    article.delete()
    return jsonify({'success': f'{article.title} has been deleted'})