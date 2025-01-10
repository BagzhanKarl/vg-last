from app.db import db

class Queue(db.Model):
    __tablename__ = 'queue'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    is_active = db.Column(db.Boolean, default=True)
    is_cancelled = db.Column(db.Boolean, default=False)
    is_completed = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, is_active):
        self.user_id = user_id
        self.is_active = is_active

    def save_to_db(self):
        data = self.query.filter_by(user_id=self.user_id).all()
        for item in data:
            item.is_active = False
            item.is_cancelled = True
        db.session.add(self)
        db.session.commit()


    def set_completed(self):
        self.is_completed = True
        self.is_active = False
        db.session.commit()