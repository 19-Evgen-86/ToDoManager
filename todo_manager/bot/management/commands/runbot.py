from django.core.management import BaseCommand
from django.db import transaction

from bot.models import TgUser
from bot.tg.client import TgClient


class Command(BaseCommand):

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient("5425707450:AAFKjl4RtyTh4CjrkLnnWXq0Xs0dl6EkC-4")
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
                chat_id = item.message.chat.id
                if item.message.text == "/start":
                    print(1)
                    # если подьзователь есть в базе, шлем приветствие:
                    if TgUser.objects.filter(tg_user=item.message.from_.id).exists():
                        tg_client.send_message(chat_id=item.message.chat.id,
                                               text=f"hello {item.message.from_.first_name}")
                    else:
                        # если пользователя нет в базе, создаем его.
                        with transaction.atomic():
                            TgUser.objects.create(tg_user=item.message.from_.id, tg_chat=item.message.chat.id)

                        tg_client.send_message(chat_id=item.message.chat.id,
                                               text=f"welcome {item.message.from_.first_name}")

                else:
                    tg_client.send_message(chat_id=chat_id, text="жду команды, хозяин!")
