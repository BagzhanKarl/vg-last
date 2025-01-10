from datetime import datetime
from app.db import db

class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50)) # user, assistant
    content = db.Column(db.Text) #message content

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, role, content, user_id):
        self.role = role
        self.content = content
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
