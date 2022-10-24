from enum import Enum
from typing import Optional

from bot.observer.base import Storage, StorageData


class MemoryStorage(Storage):
    """
    Класс для хранеия состояния бота и данных пользователя
    """
    def __init__(self):
        self.data: dict[int, StorageData] = {}

    def _get_chat_data(self, chat_id: int):
        if chat_id not in self.data:
            self.data[chat_id] = StorageData()
        return self.data[chat_id]

    def get_state(self, chat_id: int) -> Optional[Enum]:
        return self._get_chat_data(chat_id).state

    def set_state(self, chat_id: int, state: Enum):
        self._get_chat_data(chat_id).state = state

    def get_data(self, chat_id: int) -> dict:
        return self._get_chat_data(chat_id).data

    def set_data(self, chat_id: int, data: dict):
        self._get_chat_data(chat_id).data = data

    def reset(self, chat_id: int):
        self._get_chat_data(chat_id).data.clear()
        self._get_chat_data(chat_id).state = None

    def update_data(self, chat_id: int, **kwargs):
        self._get_chat_data(chat_id).data.update(**kwargs)
