import os
from random import randint

from django.core.management import BaseCommand
from django.db import transaction

from bot.models import TgUser
from bot.tg.client import TgClient


def randN(N):
    min = pow(10, N - 1)
    max = pow(10, N) - 1
    return randint(min, max)


class Command(BaseCommand):

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(os.getenv("TG_TOKEN"))
        os.environ['tg_client'] = tg_client
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
                chat_id = item.message.chat.id
                if item.message.text == "/start":
                    # если подьзователь есть в базе, шлем приветствие:
                    if TgUser.objects.filter(tg_user=item.message.from_.id).exists():
                        tg_client.send_message(chat_id=item.message.chat.id,
                                               text=f" Hello {item.message.from_.first_name}")
                    else:
                        # если пользователя нет в базе, создаем его.
                        verification_code = randN(8)
                        with transaction.atomic():
                            TgUser.objects.create(tverification_code=verification_code, chat_id=item.message.chat.id)

                        tg_client.send_message(chat_id=chat_id,
                                               text=f"Подтвердите, пожалуйста, свой аккаунт."
                                                    f" Для подтверждения необходимо ввести "
                                                    f"код: {verification_code} на сайте")

                else:
                    tg_user: TgUser = TgUser.objects.filter(chat_id=item.message.chat.id)
                    # если пользователь не прошел верификацию
                    if not tg_user.tg_user:
                        tg_client.send_message(chat_id=chat_id,
                                               text=f"Подтвердите, пожалуйста, свой аккаунт."
                                                    f" Для подтверждения необходимо ввести "
                                                    f"код: {tg_user.verification_code} на сайте")
                    else:
                        tg_client.send_message(chat_id=item.message.chat.id,
                                               text=f" do hast")
