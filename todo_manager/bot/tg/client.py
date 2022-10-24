import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    """
    Класс клиента бота
    """
    def __init__(self, token: str):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        cl = requests.get(self.get_url('getUpdates'), json={'offset': offset, 'timeout': timeout})
        return GetUpdatesResponse(**cl.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        cl = requests.post(self.get_url("sendMessage"), json={'chat_id': chat_id, "text": text})
        return SendMessageResponse(**cl.json())
