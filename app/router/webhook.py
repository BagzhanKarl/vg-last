import logging
import os
import time

import requests
from functools import wraps
from threading import Thread
from flask import Blueprint, request, jsonify

from app.db import process_webhook, Messages, User, UserLog
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
            'https://vg.assemcrm.kz/process-messages',  # ваш URL
            json={'user_id': user_id}
        )
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to notify service: {str(e)}")


@webhook_bp.route('/hook/messages', methods=['POST'])
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
    user = User.query.get(id)

    try:
        # Логируем начало генерации
        log = UserLog(
            user_id=user_id,
            event_type='generation_started',
            data={'user_id': user_id},
            status='success'
        )
        log.save_to_db()

        messages = Messages.query.filter_by(user_id=user_id).all()
        response = [{'role': m.role, 'content': m.content} for m in messages]

        assistant = AssemAI(api_key=api_key, assistant_id=assistant_id)
        ai_response = assistant.generate_response(message_history=response)

        # Логируем успешную генерацию
        log = UserLog(
            user_id=user_id,
            event_type='generation_completed',
            data={'response': ai_response},
            status='success'
        )
        log.save_to_db()

        ai_message = Messages(role='assistant', content=ai_response, user_id=user_id)
        ai_message.save_to_db()

        # Отправка сообщения
        send_message = AssemWhatsApp()
        result = send_message.send_text(ai_response, user.chat_id)

        # Логируем отправку
        log = UserLog(
            user_id=user_id,
            event_type='message_sent',
            data={'whatsapp_response': result},
            status='success' if result.get('success') else 'error'
        )
        log.save_to_db()

        return jsonify(response)

    except Exception as e:
        # Логируем ошибку
        log = UserLog(
            user_id=user_id,
            event_type='processing_error',
            data={'error': str(e)},
            status='error',
            error_message=str(e)
        )
        log.save_to_db()
        raise