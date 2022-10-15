import factory
from factory.django import DjangoModelFactory

from core.models import User
from goals.models import Goal, Board, GoalCategory, BoardParticipant, GoalComment


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = 'test4321'


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker('word')


class BoardParticipantFactory(DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = 1

class GoalCategoryFactory(DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Faker('word')
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class GoalFactory(DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Faker("word")
    category = factory.SubFactory(GoalCategoryFactory)
    user = factory.SubFactory(UserFactory)
    due_date = factory.Faker("date")


class GoalCommentFactory(DjangoModelFactory):
    class Meta:
        model = GoalComment

    user = factory.SubFactory(UserFactory)
    text = factory.Faker('word')
    goal = factory.SubFactory(GoalFactory)
