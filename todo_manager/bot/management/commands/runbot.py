import os
from datetime import datetime

from django.core.management import BaseCommand

from bot.models import TgUser
from bot.observer.base import State
from bot.observer.memory import MemoryStorage
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory
from todo_manager import settings


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.tg_client: TgClient = TgClient(settings.TG_TOKEN)
        self.storage: MemoryStorage = MemoryStorage()

    def unverified_user(self, msg: Message, user: TgUser):
        """
        обработка сообщения не верифицированного пользователя
        """
        code: str = os.urandom(10).hex()
        user.verification_code = code
        user.save(update_fields=('verification_code',))
        self.tg_client.send_message(chat_id=msg.chat.id, text=f"Подтвердите, пожалуйста, свой аккаунт."
                                                              f" Для подтверждения необходимо ввести "
                                                              f"код: {code} на сайте")

    def verified_user(self, msg: Message, user: TgUser):
        """
        обработка сообщения верифицированного пользователя
        """
        # проверяем сообщения пользователя
        match msg.text:
            # если это команда
            case value if value.startswith('/'):
                command: str = value.replace('/', '')
                match command:
                    case 'goals':
                        goals: list[str] = [f'#{goal.id} - {goal.title}' for goal in
                                            Goal.objects.filter(user_id=user.user.id).order_by('due_date')]
                        if goals:
                            self.tg_client.send_message(chat_id=msg.chat.id, text='\n'.join(goals))
                        else:
                            self.tg_client.send_message(chat_id=msg.chat.id, text="Целей нет")
                    case 'create':
                        categories = [f'#{category.id} - {category.title}'
                                      for category in GoalCategory.objects.filter(
                                board__participants__user_id=user.user.id,
                                is_deleted=False)
                                      ]
                        if categories:
                            self.tg_client.send_message(chat_id=msg.chat.id,
                                                        text="Выберите категорию\n" + "\n".join(categories))
                            self.storage.set_state(chat_id=msg.chat.id, state=State.CATEGORY_LIST_SELECTED)
                            self.storage.set_data(chat_id=msg.chat.id, data={"chat_id": msg.chat.id})
                        else:
                            self.tg_client.send_message(chat_id=msg.chat.id, text="Категорий нет")

                    case 'cancel':
                        self.storage.reset(msg.chat.id)
                        self.tg_client.send_message(chat_id=msg.chat.id, text='[canceled]')
                    case _:
                        self.tg_client.send_message(chat_id=msg.chat.id, text='неизвестная команда')
            # если цифра
            case value if value.isdigit():
                # проверяем в каком состоянии находиться бот
                match state := self.storage.get_state(msg.chat.id):
                    # если пользователь запросил списо категорий (команда /create)
                    case State.CATEGORY_LIST_SELECTED:
                        cat_id: int = int(msg.text)
                        if GoalCategory.objects.filter(board__participants__user_id=user.user.id,
                                                       is_deleted=False,
                                                       id=cat_id).exists():
                            self.storage.update_data(chat_id=msg.chat.id, cat_id=cat_id)
                            self.tg_client.send_message(chat_id=msg.chat.id, text="укажите название цели")
                            self.storage.set_state(chat_id=msg.chat.id, state=State.CATEGORY_NUM)
                        else:
                            self.tg_client.send_message(chat_id=msg.chat.id, text='категория не найдена')
                    # если пользователь выбрал категорию
                    case State.CATEGORY_NUM:
                        self.storage.update_data(chat_id=msg.chat.id, title=msg.text, due_date=datetime.now())
                        data = self.storage.get_data(msg.chat.id)
                        Goal.objects.create(title=data["title"],
                                            category_id=data['cat_id'],
                                            user_id=user.user.id,
                                            due_date=data['due_date']
                                            )
                        self.tg_client.send_message(chat_id=msg.chat.id, text='Цель создана')
                        self.storage.reset(msg.chat.id)
            case _:
                self.tg_client.send_message(chat_id=msg.chat.id, text='неизвестная команда')

    def message(self, msg: Message):
        """
        обработка сообщения пользователя
        """
        tg_user, _ = TgUser.objects.select_related("user").get_or_create(tg_chat=msg.chat.id, defaults={
            'tg_user': msg.from_.first_name
        })

        if tg_user.user:
            # подтвержденный пользователь
            self.verified_user(msg=msg, user=tg_user)
        else:
            # новый пользоватль
            self.unverified_user(msg=msg, user=tg_user)

    def handle(self, *args, **options):
        """
            запуск бота
        """
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.message(msg=item.message)
