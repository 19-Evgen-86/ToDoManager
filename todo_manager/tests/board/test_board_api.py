from rest_framework.test import APITestCase, APIClient

from tests.factories import UserFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class BoardAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_board_create_view(self):
        data = {'title': 'test'}
        response = self.client.post('/goals/board/create', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['title'], 'test')

    def test_board_list_view(self):
        response = self.client.get('/goals/board/list')
        self.assertEqual(response.status_code, 200)
