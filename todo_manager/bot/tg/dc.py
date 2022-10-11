from dataclasses import field
from typing import List, Optional

import marshmallow
from dataclasses_json import config
from pydantic import BaseModel, Field


class Chat(BaseModel):
    id: int
    first_name: str
    type: str


class MessageFrom(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str | None


class Message(BaseModel):
    message_id: int
    from_: MessageFrom = Field(alias='from')
    chat: Chat
    text: str


    class Config:
        allow_population_by_field_name = True


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: List[UpdateObj]


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message
