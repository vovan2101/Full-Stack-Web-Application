from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import base64
import os
from app import basic_auth, token_auth


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    email = db.Column(db.String(25), nullable = False, unique = True)
    password = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(32), unique = True, index = True)
    token_expiration = db.Column(db.DateTime)
    article = db.relationship('Articles', backref = 'author')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()


    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    def get_token(self):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(hours=24)
        db.session.commit()
        return self.token
        

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self, data):
        for field in data:
            if field not in {'username', 'email', 'password'}:
                continue
            if field == 'password':
                setattr(self, field, generate_password_hash(data[field]))
            else:
                setattr(self, field, data[field])
        db.session.commit()


    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': self.date_created,
        }



@token_auth.verify_token
def verify(token):
    user = User.query.filter_by(token = token).first()
    if user and user.token_expiration > datetime.utcnow():
        return user  

@basic_auth.verify_password
def verify(username, password):
    user = User.query.filter_by(username = username).first()
    if user and user.check_password(password):
        return user


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    body = db.Column(db.Text(), nullable = False)
    image_url = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for field in data:
            if field not in {'title', 'body', 'image_url', 'user_id'}:
                continue
            setattr(self, field, data[field])
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'image_url': self.image_url,
            'date_created': self.date_created,
            'author': User.query.get(self.user_id).to_dict()
        }