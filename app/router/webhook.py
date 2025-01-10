import logging
import os
import time

import requests
from functools import wraps
from threading import Thread
from flask import Blueprint, request, jsonify

from app.db import process_webhook, Messages, User
from app.service import AssemAI
from app.service.assemwhapsapp import AssemWhatsApp

api_key = os.getenv('OPENAI_API_KEY')
assistant_id = os.getenv('OPENAI_ASSISTANT_ID')

webhook_bp = Blueprint('webhook', __name__)


def async_task(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        def task():
            try:
                f(*args, **kwargs)
            except Exception as e:
                logging.error(f"Error in async task: {str(e)}")

        Thread(target=task).start()

    return wrapped


@async_task
def notify_service(user_id):
    try:
        # time.sleep(10)
        response = requests.post(
            'http://localhost:8008/process-messages',  # ваш URL
            json={'user_id': user_id}
        )
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to notify service: {str(e)}")


@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    result = process_webhook(data)

    if result is None:
        return jsonify({'error': 'Failed to process webhook'}), 500

    if result['status'] == 'success':
        notify_service(result['user_id'])
    return jsonify(result), 200

@webhook_bp.route('/process-messages', methods=['POST'])
def process_messages_checker():
    user_id = request.json['user_id']
    user = User.query.filter_by(id=user_id).first()
    messages = Messages.query.filter_by(user_id=user_id).all()
    response = []
    for message in messages:
        response.append({
            'role': message.role,
            'content': message.content,
        })
    assistant = AssemAI(
        api_key=api_key,
        assistant_id=assistant_id,
    )
    ai = assistant.generate_response(message_history=response)
    ai_message = Messages(role='assistant',content=ai,user_id=user_id)
    ai_message.save_to_db()
    send_message = AssemWhatsApp()
    send_message.send_text(ai, user.chat_id)
    return jsonify(response)