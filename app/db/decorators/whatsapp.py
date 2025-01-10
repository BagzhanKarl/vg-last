from typing import Dict, Optional, Union
from datetime import datetime

from app.db import User, Messages, Queue


class WebhookHandler:
    def __init__(self, data: Dict):
        """
        Инициализация обработчика веб-хуков

        Args:
            data (Dict): Данные веб-хука
        """
        self.data = data
        self.message = data.get('messages', [{}])[0]

    def is_valid_message(self) -> bool:
        """Проверка, является ли сообщение текстовым"""
        return (
                self.message.get('type') == 'text' and
                'text' in self.message and
                'body' in self.message['text']
        )

    def get_message_text(self) -> str:
        """Получение текста сообщения или генерация текста для нетекстовых типов"""
        if not self.is_valid_message():
            message_type = self.message.get('type', 'unknown')
            return f"[Получено {message_type} сообщение]"
        return self.message['text']['body']

    def get_user_data(self) -> Dict[str, str]:
        """Извлечение данных пользователя из сообщения"""
        return {
            'name': self.message.get('from_name', ''),
            'phone': self.message.get('from', ''),
            'chat_id': self.message.get('chat_id', '')
        }
    def check_sender(self) -> bool:
        return (
            self.message.get('from_me') == False
        )


def process_webhook(webhook_data: Dict) -> Union[Dict, None]:
    """
    Обработка входящего веб-хука

    Args:
        webhook_data (Dict): Данные веб-хука

    Returns:
        Dict: Результат обработки или None в случае ошибки
    """
    try:
        handler = WebhookHandler(webhook_data)

        # Получаем данные пользователя
        user_data = handler.get_user_data()

        for_me = handler.check_sender()
        if for_me:

            # Ищем пользователя по телефону
            existing_user = User.query.filter_by(phone=user_data['phone']).first()

            if not existing_user:
                # Создаем нового пользователя
                user = User(
                    name=user_data['name'],
                    phone=user_data['phone'],
                    chat_id=user_data['chat_id']
                )
                user.save_to_db()
            else:
                user = existing_user

            # Сохраняем сообщение
            message = Messages(
                role='user',
                content=handler.get_message_text(),
                user_id=user.id
            )
            message.save_to_db()

            set_queue = Queue(
                user_id=user.id,
                is_active=True
            )
            set_queue.save_to_db()

            return {
                'status': 'success',
                'user_id': user.id,
                'is_text_message': handler.is_valid_message(),
                'queue_id': set_queue.id,
            }
        else:
            return {
                'status': 'fail',
                'detail': 'Сообщению отправили мы!',
            }

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return None

