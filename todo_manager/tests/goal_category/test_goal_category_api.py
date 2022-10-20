from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from goals.models import Board, GoalCategory, BoardParticipant
from tests.factories import UserFactory, BoardFactory, BoardParticipantFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class GoalCategoryAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)

    def test_goals_category_create_view(self):
        board: Board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.owner)
        data = {'title': 'test_category', 'board': board.id}
        response = self.client.post('/goals/goal_category/create', data)
        self.assertEqual(response.status_code, 201)
        goal_category: GoalCategory = GoalCategory.objects.last()
        expect_data = {'board': board.id,
                       'created': timezone.localtime(goal_category.created).isoformat(),
                       'id': goal_category.id,
                       'is_deleted': False,
                       'title': 'test_category',
                       'updated': timezone.localtime(goal_category.updated).isoformat()}
        self.assertEqual(response.json(), expect_data)
