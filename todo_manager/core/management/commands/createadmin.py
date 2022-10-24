import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from core.models import User

load_dotenv()


class Command(BaseCommand):
    """
    Создание суперпользователя при первом запуске приложения
    """

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username: str = os.getenv("ADMIN", 'admin')
            password: str = os.getenv("ADMIN_PASSWORD", 'admin')
            print(f'Creating account for {username}')
            admin: User = User.objects.create_superuser(username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Administrator account cannot be created because there are already registered users in the system')
