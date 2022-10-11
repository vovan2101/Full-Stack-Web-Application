from app import db
from datetime import datetime, timedelta


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
        from app.blueprints.auth.models import User
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'image_url': self.image_url,
            'date_created': self.date_created,
            'author': User.query.get(self.user_id).to_dict()
        }