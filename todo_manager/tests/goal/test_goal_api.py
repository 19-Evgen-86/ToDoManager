from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from goals.models import GoalCategory, Board, BoardParticipant
from tests.factories import UserFactory, GoalCategoryFactory, GoalFactory, BoardFactory, BoardParticipantFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class GoalAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)



    def test_goal_create_view(self):
        board: Board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.owner)
        category: GoalCategory = GoalCategoryFactory(board=board, user=self.user)
        data = {'title': 'test_category', 'category': category.pk, 'due_date': timezone.now()}
        response = self.client.post(reverse('goal_create'), data)
        self.assertEqual(response.status_code, 201)
