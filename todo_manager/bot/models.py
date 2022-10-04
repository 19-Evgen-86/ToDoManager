from django.db import models

from core.models import User


# Create your models here.
class TgUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    tg_user = models.IntegerField()
    tg_chat = models.IntegerField()
    verification_code = models.IntegerField()
