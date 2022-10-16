from rest_framework.test import APITestCase, APIClient

from tests.factories import UserFactory, GoalFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class GoalCommentAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_goal_comment_create_view(self):
        goal = GoalFactory()
        data = {'text': 'test_comment', 'goal': goal.id}
        response = self.client.post('/goals/goal_comment/create', data)
        self.assertEqual(response.status_code, 201)

    def test_goal_comment_list_view(self):
        response = self.client.get('/goals/goal_comment/list')
        self.assertEqual(response.status_code, 200)
