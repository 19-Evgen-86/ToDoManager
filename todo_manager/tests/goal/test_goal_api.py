from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from tests.factories import UserFactory, GoalCategoryFactory, GoalFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class GoalAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_goal_create_view(self):
        category = GoalCategoryFactory()
        data = {'title': 'test_category', 'board': category.id, 'due_date': timezone.now()}
        response = self.client.post('/goals/goal/create', data)
        self.assertEqual(response.status_code, 201)

    def test_goal_list_view(self):
        goals = GoalFactory.create_batch(2)
        response = self.client.get('/goals/goal/list')
        self.assertEqual(response.status_code, 200)
