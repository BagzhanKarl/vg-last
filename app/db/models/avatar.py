from app.db import db

class Avatar(db.Model):
    __tablename__ = 'avatar'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    how_to_behave = db.Column(db.Text, nullable=False)
    role_or_position = db.Column(db.Text, nullable=False)
    first_message = db.Column(db.Text, nullable=False)
    additional_info = db.Column(db.Text, nullable=False)
    lang = db.Column(db.String(150), nullable=False)
    temp = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, name, how_to_behave, additional_info, role, lang, first_message, temp, is_active):
        self.name = name
        self.how_to_behave = how_to_behave
        self.additional_info = additional_info
        self.is_active = is_active
        self.lang = lang
        self.temp = temp
        self.first_message = first_message
        self.role_or_position = role

    def save_to_db(self):
        other = self.query.all()
        for item in other:
            item.is_active = False
        db.session.add(self)
        db.session.commit()