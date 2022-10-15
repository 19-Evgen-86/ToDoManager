from pytest_factoryboy import register

from tests.factories import BoardFactory, BoardParticipantFactory, GoalCategoryFactory, GoalFactory, \
    GoalCommentFactory, UserFactory
# pytest_plugins = "tests.fixtures"

register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(GoalCategoryFactory)
register(GoalFactory)
register(GoalCommentFactory)
