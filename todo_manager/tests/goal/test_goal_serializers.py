from django.test import TestCase
from django.utils import timezone

from goals.models import Goal
from goals.serializers import GoalCreateSerializer
from tests.factories import GoalFactory


class GoalSerializersTestCase(TestCase):

    def test_create_goal_serializer(self):
        """
        GoalCreateSerializer
        """
        goal: Goal = GoalFactory()
        data = GoalCreateSerializer(goal).data
        ex_data = {'id': goal.id, 'created': timezone.localtime(goal.created).isoformat(),
                   'updated': timezone.localtime(goal.updated).isoformat(),
                   'title': goal.title, 'description': goal.description, 'status': goal.status,
                   'priority': goal.priority,
                   'due_date': goal.due_date,
                   'is_deleted': False, 'category': goal.category.id}
        self.assertEqual(ex_data, data)
