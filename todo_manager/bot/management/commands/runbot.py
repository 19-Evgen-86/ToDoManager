import os

from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from todo_manager import settings


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
            'tg_user': msg.from_.first_name
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
                print(item.message)


