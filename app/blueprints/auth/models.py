import os
import base64
from datetime import datetime, timedelta
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


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

