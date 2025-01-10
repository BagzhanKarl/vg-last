import time

import openai
from typing import List, Dict, Optional

from openai import OpenAI

class AssemAI:
    def __init__(self, assistant_id: str, api_key: str):
        """
        Инициализация менеджера ассистента

        Args:
            assistant_id (str): ID ассистента в OpenAI
            api_key (str): API ключ OpenAI
        """
        self.assistant_id = assistant_id
        self.client = OpenAI(api_key=api_key)

    def update_assistant_instructions(self, new_instructions: str, temp: float) -> Dict:
        """
        Обновление инструкций ассистента

        Args:
            new_instructions (str): Новые инструкции для ассистента

        Returns:
            Dict: Обновленная информация об ассистенте
        """
        try:
            updated_assistant = self.client.beta.assistants.update(
                assistant_id=self.assistant_id,
                instructions=new_instructions,
                temperature=temp
            )
            return updated_assistant
        except Exception as e:
            raise Exception(f"Ошибка при обновлении инструкций: {str(e)}")

    def generate_response(self,
                          message_history: List[Dict[str, str]],
                          max_retries: int = 3,
                          timeout: int = 60) -> str:
        """
        Генерация ответа от ассистента

        Args:

            message_history (List[Dict[str, str]]): История сообщений в формате
                [{"role": "user/assistant", "content": "текст сообщения"}, ...]
            max_retries (int): Максимальное количество попыток получения ответа
            timeout (int): Таймаут ожидания ответа в секундах

        Returns:
            str: Ответ ассистента
        """
        try:
            thread = self.client.beta.threads.create(
                messages=message_history,
            )
            run = self.client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=self.assistant_id)
            while run.status != 'completed':
                run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                time.sleep(1)
                print('Waiting')

            else:
                print('Done')

            message = self.client.beta.threads.messages.list(thread_id=thread.id)
            messages = message.data
            latest = messages[0]
            return latest.content[0].text.value

        except Exception as e:
            raise Exception(f"Ошибка при генерации ответа: {str(e)}")