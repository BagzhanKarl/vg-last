from datetime import datetime

from app.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    chat_id = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, name, phone, chat_id):
        self.name = name
        self.phone = phone
        self.chat_id = chat_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
