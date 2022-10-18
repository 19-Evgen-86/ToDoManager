from rest_framework.test import APITestCase, APIClient

from tests.factories import UserFactory, BoardFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class GoalCategoryAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_goals_category_create_view(self):
        board = BoardFactory()
        data = {'title': 'test_category', 'board': board.id}
        response = self.client.post('/goals/goal_category/create', data)
        self.assertEqual(response.status_code, 201)


