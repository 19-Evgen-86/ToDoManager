from django.db import models
from django.utils import timezone

from core.models import User


class DateFieldsMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class GoalCategory(DateFieldsMixin):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)

    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    def __str__(self):
        return self.title


class Goal(DateFieldsMixin):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.CharField(verbose_name='Описание', max_length=255)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='Приоритет', choices=Priority.choices,
                                                default=Priority.medium)
    due_date = models.DateTimeField(verbose_name='Дата дедлайн')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')

    def __str__(self):
        return self.title


class GoalComment(DateFieldsMixin):
    class Meta:
        verbose_name = "Комментраий"
        verbose_name_plural = "Комментраии"

    text = models.TextField(verbose_name='Комментарий')
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.CASCADE)

    def __str__(self):
        return f"коментарий к {self.goal.title}"
