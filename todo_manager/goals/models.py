from django.db import models
from django.utils import timezone

from core.models import User


class DateFieldsMixin(models.Model):
    """
    вспомогательный миксин класс с общими полями.
    """

    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name='Дата последнего обновления')

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Board(DateFieldsMixin):
    """
    Модель доски целей
    """

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(DateFieldsMixin):
    """
    Модель участников для доски целей
    """

    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )


class GoalCategory(DateFieldsMixin):
    """
    модель категорий целей
    """

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name="Название", max_length=255, unique=True)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False, verbose_name='Удалена')
    board = models.ForeignKey(
        Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )

    def __str__(self):
        return self.title


class Goal(DateFieldsMixin):
    """
    Модель цели
    """

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

    title = models.CharField(verbose_name="Название", max_length=255, unique=True)
    description = models.CharField(verbose_name='Описание', max_length=255, null=True)
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
    """
     Модель комментариев к цели
    """

    class Meta:
        verbose_name = "Комментраий"
        verbose_name_plural = "Комментраии"

    user = models.ForeignKey(User, verbose_name="Автор коментария", on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.CASCADE)

    def __str__(self):
        return f"коментарий к {self.goal.title}"
