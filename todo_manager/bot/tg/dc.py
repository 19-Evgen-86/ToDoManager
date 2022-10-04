from dataclasses import dataclass
from typing import List,Optional

import marshmallow

"""
"message":{"message_id":1,"from":
{"id":332825939,"is_bot":false,"first_name":"\u041c\u0430\u043a\u0441","language_code":"ru"},
"chat":{"id":332825939,"first_name":"\u041c\u0430\u043a\u0441","type":"private"},
"date":1664637003,"text":"/start",
"entities":[{"offset":0,"length":6,"type":"bot_command"}]}}"""


@dataclass()
class Chat:
    id: int
    first_name: str
    type: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass()
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    language_code: Optional[str]
    username: Optional[str]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass()
class Message:
    message_id: int
    from_: MessageFrom
    chat: Chat
    text: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass()
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE
