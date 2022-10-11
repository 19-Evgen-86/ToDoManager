from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional

from pydantic import BaseModel


class Storage(ABC):
    @abstractmethod
    def get_state(self, chat_id: int) -> Optional[Enum]:
        raise NotImplementedError

    @abstractmethod
    def set_state(self, chat_id: int, state: Enum):
        raise NotImplementedError

    @abstractmethod
    def get_data(self, chat_id: int):
        raise NotImplementedError

    @abstractmethod
    def set_data(self, chat_id: int, data: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    def reset(self, chat_id: int):
        raise NotImplementedError

    @abstractmethod
    def update_data(self, chat_id: int, **kwargs):
        raise NotImplementedError


class StorageData(BaseModel):
    data: dict = {}
    state: Optional[Enum]


class State(Enum):
    CATEGORY_LIST_SELECTED = auto()
    CATEGORY_NUM = auto()



