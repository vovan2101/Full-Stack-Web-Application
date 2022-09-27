from enum import unique
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(25), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    article = db.relationship('Articles', backref = 'author')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'article', 'data_created')

user_chema = UserSchema()


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    body = db.Column(db.Text(), nullable = False)
    image_url = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, title, body, image_url):
        self.title = title
        self.body = body
        self.image_url = image_url

class ArticlesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'image_url', 'date_created', 'user_id')

article_chema = ArticlesSchema()
articles_chema = ArticlesSchema(many=True)

