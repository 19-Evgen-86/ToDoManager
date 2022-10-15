from typing import List

from pydantic import BaseModel, Field


class Chat(BaseModel):
    """
    модель чата бота
    """
    id: int
    first_name: str
    type: str


class MessageFrom(BaseModel):
    """
      модель отправителя сообщения бота
      """
    id: int
    is_bot: bool
    first_name: str
    username: str | None


class Message(BaseModel):
    """
      модель сообщения бота
      """
    message_id: int
    from_: MessageFrom = Field(alias='from')
    chat: Chat
    text: str

    class Config:
        allow_population_by_field_name = True


class UpdateObj(BaseModel):
    """
    Модель объектв входящее обновление от бота
    """
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    """
     Модель входящего сообщения от бота
    """
    ok: bool
    result: List[UpdateObj]


class SendMessageResponse(BaseModel):
    """
       Модель объекта отправленного сообщения пользователю
    """
    ok: bool
    result: Message
