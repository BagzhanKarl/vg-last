# app/db/models/logs.py
from datetime import datetime
from app.db import db

class UserLog(db.Model):
    __tablename__ = 'user_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_type = db.Column(db.String(50))  # webhook_received, response_generated, message_sent
    data = db.Column(db.JSON)
    status = db.Column(db.String(50))  # success, error
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()