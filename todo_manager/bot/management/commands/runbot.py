import os
from random import randint

from django.core.management import BaseCommand
from django.db import transaction
from dotenv import load_dotenv

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from todo_manager import settings

load_dotenv()


def randN(N):
    min = pow(10, N - 1)
    max = pow(10, N) - 1
    return randint(min, max)


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.tg_client: TgClient = TgClient(settings.TG_TOKEN)

    def unverified_user(self, msg: Message, user: TgUser):
        code = os.urandom(10).hex()
        user.verification_code = code
        user.save(update_fields=('verification_code',))
        self.tg_client.send_message(chat_id=msg.chat.id, text=f"Подтвердите, пожалуйста, свой аккаунт."
                                                              f" Для подтверждения необходимо ввести "
                                                              f"код: {code} на сайте")

    def message(self, msg: Message):
        tg_user, _ = TgUser.objects.select_related("user").get_or_create(tg_chat=msg.chat.id, defaults={
            'tg_user': msg.from_.username
        })

        if tg_user.user:
            # подтвержденный пользователь
            self.tg_client.send_message(chat_id=msg.chat.id, text=msg.text)
        else:
            # новый пользоватль
            self.unverified_user(msg=msg, user=tg_user)

    def handle(self, *args, **options):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.message(msg=item.message)

        #     self.tg_client.send_message(chat_id=item.message.chat.id, text=item.message.text)
        #
        #     # если подьзователь есть в базе, шлем приветствие:
        #     if TgUser.objects.filter(tg_user=item.message.from_.id).exists():
        #         tg_client.send_message(chat_id=item.message.chat.id,
        #                                text=f" Hello {item.message.from_.first_name}")
        #     else:
        #         # если пользователя нет в базе, создаем его.
        #         verification_code = randN(8)
        #         with transaction.atomic():
        #             if not TgUser.objects.filter(tg_chat=item.message.chat.id).exists():
        #                 TgUser.objects.create(verification_code=verification_code,
        #                                       tg_chat=item.message.chat.id)
        #             else:
        #                 TgUser.objects.filter(tg_chat=item.message.chat.id).update(
        #                     verification_code=verification_code)
        #
        #         tg_client.send_message(chat_id=item.message.chat.id,
        #                                text=f"Подтвердите, пожалуйста, свой аккаунт."
        #                                     f" Для подтверждения необходимо ввести "
        #                                     f"код: {verification_code} на сайте")
        #
        # else:
        #     tg_user: TgUser = TgUser.objects.get(tg_chat=item.message.chat.id)
        #     # если пользователь не прошел верификацию
        #     if not tg_user.tg_user:
        #         tg_client.send_message(chat_id=item.message.chat.id,
        #                                text=f"Подтвердите, пожалуйста, свой аккаунт."
        #                                     f" Для подтверждения необходимо ввести "
        #                                     f"код: {tg_user.verification_code} на сайте")
        #     else:
        #         tg_client.send_message(chat_id=item.message.chat.id,
        #                                text=f" do hast")
