# app/db/models/balance.py
from app.db import db
from datetime import datetime
import tiktoken

class Balance(db.Model):
    __tablename__ = 'balance'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tokens_in = db.Column(db.Integer)
    tokens_out = db.Column(db.Integer)
    cost_tenge = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)

def calculate_tokens_and_cost(text: str) -> tuple:
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens = len(encoding.encode(text))
    # $2.50 за 1M токенов ≈ 1125 тенге
    cost = (tokens * 1125) / 1_000_000
    return tokens, cost