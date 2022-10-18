from django.test import TestCase
from django.utils import timezone

from goals.models import GoalCategory
from goals.serializers import CreateGoalsCategorySerializer
from tests.factories import GoalCategoryFactory


class GoalCategorySerializersTestCase(TestCase):

    def test_create_goals_category_serializer(self):
        """
        CreateGoalsCategorySerializer
        """
        goal_category: GoalCategory = GoalCategoryFactory()
        data = CreateGoalsCategorySerializer(goal_category).data
        ex_data = {"id": goal_category.id,
                   'is_deleted': False,
                   "title": goal_category.title,
                   "board": goal_category.board.id,
                   "created": timezone.localtime(goal_category.created).isoformat(),
                   "updated": timezone.localtime(goal_category.updated).isoformat()}
        self.assertDictEqual(ex_data, data)
