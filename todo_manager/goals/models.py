
from django.db import models
from django.utils import timezone

from core.models import User


class GoalsCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    create = models.DateTimeField(verbose_name="Дата создания")
    update = models.DateTimeField(verbose_name='Дата последнего обновления')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    def save(self, *args, **kwargs):
        if not self.id:
            self.create = timezone.now()
        self.update = timezone.now()
        return super().save(*args, **kwargs)



