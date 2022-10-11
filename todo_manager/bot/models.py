from django.db import models

from core.models import User


# Create your models here.
class TgUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, default=None)
    tg_user = models.CharField(max_length=255, null=True, blank=True, default=None)
    tg_chat = models.BigIntegerField()
    verification_code = models.CharField(max_length=255, default=None, null=True, blank=True)
