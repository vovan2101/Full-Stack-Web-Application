from app import app,db
from flask import jsonify, request
from app.models import Articles, ArticlesSchema, article_chema , articles_chema


@app.route('/get', methods = ['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_chema.dump(all_articles)
    return jsonify(results)


@app.route('/get/<id>/', methods = ['GET'])
def article_details(id):
    article = Articles.query.get(id)
    return article_chema.jsonify(article)


@app.route('/add', methods= ['POST'])
def add_article():
    title = request.json['title']
    body = request.json['body']
    image_url = request.json['image_url']

    articles = Articles(title, body, image_url)
    db.session.add(articles)
    db.session.commit()
    return article_chema.jsonify(articles)


@app.route('/update/<id>/', methods = ['PUT'])
def update_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    body = request.json['body']
    image_url = request.json['image_url']

    article.title = title
    article.body = body
    article.image_url = image_url

    db.session.commit()
    return article_chema.jsonify(article)


@app.route('/delete/<id>/', methods = ['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return article_chema.jsonify(article)